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
# ===== TELEGRAM VERIFY =====
BOT_TOKEN = "7955185832:AAH4_TJyi_P78BFkHnBl32d3CgD4sdZ7Gxo"
CHANNEL_USERNAME = "@helproot"
# ===== COS =====
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(
    f"\n{CYAN}{BOLD}╔══════════════════════════════════════╗{RESET}\n"
    f"{CYAN}{BOLD}║{RESET}    {WHITE}{BOLD}[V{version}] For issues or feedback{RESET}   {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╠══════════════════════════════════════╣{RESET}\n"
    f"{CYAN}{BOLD}║  {RESET} {YELLOW}Telegram Channel:{RESET} {GREEN}t.me/helproot{RESET}    {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╠══════════════════════════════════════╣{RESET}\n"
    f"{CYAN}{BOLD}║   {RESET} {YELLOW}Telegram Bot:{RESET} {GREEN}@HelpRootAppBot{RESET}     {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╠══════════════════════════════════════╣{RESET}\n"
    f"{CYAN}{BOLD}║         {RESET} {YELLOW}Made By:{RESET} {GREEN}@HelpRoot{RESET}          {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╚══════════════════════════════════════╝{RESET}\n"
)
def check_telegram_join(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"

    try:
        r = requests.get(url, params={
            "chat_id": CHANNEL_USERNAME,
            "
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

        r = 
U_apply = api + "apply/bl-auth"
U_info = api + "user/data"

headers = {
  'User-Agent': User,
  'Accept-Encoding': "gzip",
  'Content-Type': "application/json",
  'content-type': "application/json; charset=utf-8",
  'Cookie': f"new_bbs_serviceToken={new_bbs_serviceToken};versionCode={versionCode};versionName={versionName};deviceId={deviceId};"
}

# ===== COLORS =====
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ===== INFO BOX =====
info = requests.get(U_info, headers=headers).json()['data']

print(
    f"\n{CYAN}{BOLD}╔══════════════════════════════════════╗{RESET}\n"
    f"{CYAN}{BOLD}║{RESET}            {WHITE}{BOLD}ACCOUNT INFO{RESET}              {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╠══════════════════════════════════════╣{RESET}\n"
    f"{CYAN}{BOLD}║        {RESET} {YELLOW}Days in Community:{RESET} {WHITE}{info['registered_day']}{RESET}         {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}║        {RESET} {YELLOW}Level:{RESET} {WHITE}LV{info['level_info']['level']} {info['level_info']['level_title']}{RESET}        {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}║        {RESET} {YELLOW}Next Level Points:{RESET} {WHITE}{info['level_info']['max_value'] - info['level_info']['current_value']}{RESET}        {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}║        {RESET} {YELLOW}Points:{RESET} {WHITE}{info['level_info']['current_value']}{RESET}                    {CYAN}{BOLD}║{RESET}\n"
    f"{CYAN}{BOLD}╚══════════════════════════════════════╝{RESET}\n"
)


def state_request():
    print(
        f"{GREEN}{BOLD}╔══════════════════════════════════════╗{RESET}\n"
        f"{GREEN}{BOLD}║{RESET}             {WHITE}{BOLD}ACCOUNT STATE{RESET}            {GREEN}{BOLD}║{RESET}\n"
        f"{GREEN}{BOLD}╚══════════════════════════════════════╝{RESET}"
    )

    try:
        state = requests.get(U_state, headers=headers).json().get("data", {})
        is_ = state.get("is_pass")
        button_ = state.get("button_state")
        deadline_ = state.get("deadline_format", "")

        if is_ == 1:
            exit(f"{GREEN}✔ Unlock access granted till {deadline_} (Beijing time){RESET}\n")

        msg = {
            1: f"{YELLOW}➤ Apply for bootloader unlocking{RESET}\n",
            2: f"{RED}✖ Account Error, try again after {deadline_} (mm/dd){RESET}\n",
            3: f"{RED}✖ Account must be registered over 30 days{RESET}\n"
        }

        print(msg.get(button_, ""))

        if button_ in [2, 3]:
            exit()

    except Exception as e:
        exit(f"{RED}state: {e}{RESET}")


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
