#!/usr/bin/python

versionCode = '500418'
versionName = '5.4.18'

import os
import importlib

while True:
    for lib in ['requests', 'ntplib']:
        try:
            importlib.import_module(lib)
        except ModuleNotFoundError:
            os.system(f'pip install {lib}')
            break
    else:
        break

import requests, json, hashlib, urllib.parse, time, sys, os, base64, ntplib
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlparse, quote

version = "1.5.3"

print(f"\n[V{version}] For issues or feedback:\n- Telegram: t.me/helproot\n")

User = "okhttp/4.12.0"
headers = {"User-Agent": User}

def login():
    base_url = "https://account.xiaomi.com"
    sid = "18n_bbs_global"

    user = input('\nEnter Mi Account ID: ')
    pwd = input('\nEnter Mi Account PWD: ')
    hash_pwd = hashlib.md5(pwd.encode()).hexdigest().upper()
    cookies = {}

    def parse(res): return json.loads(res.text[11:])

    r = requests.get(f"{base_url}/pass/serviceLogin", params={'sid': sid, '_json': True}, headers=headers, cookies=cookies)
    cookies.update(r.cookies.get_dict())

    deviceId = cookies["deviceId"]

    data = {k: v[0] for k, v in parse_qs(urlparse(parse(r)['location']).query).items()}
    data.update({'user': user, 'hash': hash_pwd})

    r = requests.post(f"{base_url}/pass/serviceLoginAuth2", data=data, headers=headers, cookies=cookies)
    cookies.update(r.cookies.get_dict())
    res = parse(r)

    if res["code"] == 70016: exit("invalid user or pwd")
    if 'notificationUrl' in res:
        url = res['notificationUrl']
        if any(x in url for x in ['callback','SetEmail','BindAppealOrSafePhone']): exit(url)

        cookies.update({"NativeUserAgent": base64.b64encode(User.encode()).decode()})
        params = parse_qs(urlparse(url).query)
        cookies.update(requests.get(f"{base_url}/identity/list", params=params, headers=headers, cookies=cookies).cookies.get_dict())

        email = parse(requests.get(f"{base_url}/identity/auth/verifyEmail", params={'_json': True}, cookies=cookies, headers=headers))['maskedEmail']
        quota = parse(requests.post(f"{base_url}/identity/pass/sms/userQuota", data={'addressType': 'EM', 'contentType': 160040}, cookies=cookies, headers=headers))['info']
        print(f"Account Authentication\nemail: {email}, Remaining attempts: {quota}")
        input("\nPress Enter to send the verification code")

        code_res = parse(requests.post(f"{base_url}/identity/auth/sendEmailTicket", cookies=cookies, headers=headers))

        if code_res["code"] == 0: print(f"\nVerification code sent to your {email}")
        elif code_res["code"] == 70022: exit("Sent too many codes. Try again tomorrow.")
        else: exit(code_res)

        while True:
            ticket = input("Enter code: ").strip()
            v_res = parse(requests.post(f"{base_url}/identity/auth/verifyEmail", data={'ticket':ticket, 'trust':True}, cookies=cookies, headers=headers))
            if v_res["code"] == 70014: print("Verification code error")
            elif v_res["code"] == 0:
                cookies.update(requests.get(v_res['location'], headers=headers, cookies=cookies).history[1].cookies.get_dict())
                cookies.pop("pass_ua", None)
                break
            else: exit(v_res)

        r = requests.get(f"{base_url}/pass/serviceLogin", params={'_json': "true", 'sid': sid}, cookies=cookies, headers=headers)
        res = parse(r)

    region = json.loads(requests.get(f"https://account.xiaomi.com/pass/user/login/region", headers=headers, cookies=cookies).text[11:])["data"]["region"]    

    nonce, ssecurity = res['nonce'], res['ssecurity']
    res['location'] += f"&clientSign={quote(base64.b64encode(hashlib.sha1(f'nonce={nonce}&{ssecurity}'.encode()).digest()))}"
    serviceToken = requests.get(res['location'], headers=headers, cookies=cookies).cookies.get_dict()

    micdata = {"userId": res['userId'], "new_bbs_serviceToken": serviceToken["new_bbs_serviceToken"], "region": region, "deviceId": deviceId}
    with open("micdata.json", "w") as f: json.dump(micdata, f)
    return micdata

try:
    with open('micdata.json') as f:
        micdata = json.load(f)
    if not all(micdata.get(k) for k in ("userId", "new_bbs_serviceToken", "region", "deviceId")):
        raise ValueError
    print(f"\nAccount ID: {micdata['userId']}")
    input("Press 'Enter' to continue.\nPress 'Ctrl' + 'd' to log out.")
except (FileNotFoundError, json.JSONDecodeError, EOFError, ValueError):
    if os.path.exists('micdata.json'):
        os.remove('micdata.json')
    micdata = login()

new_bbs_serviceToken = micdata["new_bbs_serviceToken"]

deviceId = micdata["deviceId"]

print(f"\nAccount Region: {micdata['region']}")

api = "https://sgp-api.buy.mi.com/bbs/api/global/"

U_state = api + "user/bl-switch/state"
U_apply = api + "apply/bl-auth"
U_info = api + "user/data"

headers = {
  'User-Agent': User,
  'Accept-Encoding': "gzip",
  'Content-Type': "application/json",
  'content-type': "application/json; charset=utf-8",
  'Cookie': f"new_bbs_serviceToken={new_bbs_serviceToken};versionCode={versionCode};versionName={versionName};deviceId={deviceId};"
}

print("\n[INFO]:")
info = requests.get(U_info, headers=headers).json()['data']

print(f"{info['registered_day']} days in Community")
print(f"LV{info['level_info']['level']} {info['level_info']['level_title']}")
print(f"{info['level_info']['max_value'] - info['level_info']['current_value']} more points to the next level")
print(f"Points: {info['level_info']['current_value']}")

def state_request():
    print("\n[STATE]:")
    try:
        state = requests.get(U_state, headers=headers).json().get("data", {})
        is_ = state.get("is_pass")
        button_ = state.get("button_state")
        deadline_ = state.get("deadline_format", "")
        if is_ == 1:
            exit(f"You have been granted access to unlock until Beijing time {deadline_} (mm/dd/yyyy)\n")
        msg = {
            1: "Apply for unlocking\n",
            2: f"Account Error Please try again after {deadline_} (mm/dd)\n",
            3: "Account must be registered over 30 days\n"
        }
        print(msg.get(button_, ""))
        if button_ in [2, 3]:
            exit()
    except Exception as e:
        exit(f"state: {e}")

state_request()

def apply_request():
    print("\n[APPLY]:")
    try:
        apply = requests.post(U_apply, data=json.dumps({"is_retry": True}), headers=headers)
        print(f"Server response time: {apply.headers['Date']}")
        if apply.json().get("code") != 0:
            exit(apply.json())
        data_ = apply.json().get("data", {}) or {}
        apply_ = data_.get("apply_result", 0)
        deadline_ = data_.get("deadline_format", "")
        messages = {
            1: "Application Successful",
            4: f"\nAccount Error Please try again after {deadline_} (mm/dd)\n",
            3: f"\nApplication quota limit reached, please try again after {deadline_.split()[0]} (mm/dd) {deadline_.split()[1]} (GMT+8)\n",
            5: "\nApplication failed. Please try again later\n",
            6: "\nPlease try again in a minute\n",
            7: "\nPlease try again later\n"
        }
        print(messages.get(apply_, ""))
        if apply_ == 1:
            state_request()
        elif apply_ in [4, 5, 6, 7]:
            exit()
        elif apply_ == 3:
            return 1
    except Exception as e:
        exit(f"apply: {e}")


def get_ntp_time(servers=["pool.ntp.org", "time.google.com", "time.windows.com"]):
    client = ntplib.NTPClient()
    for server in servers:
        try:
            response = client.request(server, version=3, timeout=5)
            return datetime.fromtimestamp(response.tx_time, timezone.utc)
        except Exception:
            continue
    return datetime.now(timezone.utc)

def get_beijing_time():
    utc_time = get_ntp_time()
    return utc_time.astimezone(timezone(timedelta(hours=8)))

def precise_sleep(target_time, precision=0.01):
    while True:
        diff = (target_time - datetime.now(target_time.tzinfo)).total_seconds()
        if diff <= 0:
            return
        sleep_time = max(min(diff - precision/2, 1), precision)
        time.sleep(sleep_time)

def measure_latency(url, samples=5):
    latencies = []
    for _ in range(samples):
        try:
            start = time.perf_counter()
            requests.post(url, headers=headers, data='{}', timeout=2)
            latencies.append((time.perf_counter() - start) * 1000)
        except Exception:
            continue

    if len(latencies) < 3:
        return 200

    latencies.sort()
    trim = int(len(latencies) * 0.2)
    trimmed = latencies[trim:-trim] if trim else latencies
    return sum(trimmed)/len(trimmed) * 1.3

def schedule_daily_task():
    beijing_tz = timezone(timedelta(hours=8))

    while True:
        now = get_beijing_time()
        target = now.replace(hour=23, minute=57, second=0, microsecond=0)
        if now >= target:
            target += timedelta(days=1)

        print(f"\nNext execution at: {target.strftime('%Y-%m-%d %H:%M:%S.%f')} CST")
        while datetime.now(beijing_tz) < target:
            time_left = (target - datetime.now(beijing_tz)).total_seconds()
            if time_left > 300:
                time.sleep(60)
            else:
                precise_sleep(target)

        latency = measure_latency(U_apply)
        execution_time = target + timedelta(minutes=3) - timedelta(milliseconds=latency)

        print(f"Adjusted execution time: {execution_time.strftime('%H:%M:%S.%f')}")
        precise_sleep(execution_time)

        result = apply_request()
        if result == 1:
            return 1


while True:
    result = schedule_daily_task()
    if result != 1:
        break
