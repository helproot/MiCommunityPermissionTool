#!/data/data/com.termux/files/usr/bin/bash

# Colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

clear

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════╗"
echo "║        ⚡ Mi Community Bootloader ⚡       ║"
echo "║        Unlock Permission Installer         ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${RESET}"


sleep 0.5
echo -e "${BLUE}[•] Preparing environment...${RESET}"

# Update packages
pkg update -y > /dev/null 2>&1

# Install python
echo -e "${YELLOW}[•] Checking Python...${RESET}"
pkg install python -y > /dev/null 2>&1

# Create hidden folder
mkdir -p $HOME/.@helproot

echo -e "${BLUE}[•] Downloading core tool...${RESET}"

# Download main script
curl -L https://raw.githubusercontent.com/danger24bot/miunlock/main/MiCommunityTool.py \
-o $HOME/.@helproot/MiCommunityTool.py > /dev/null 2>&1

# Check download
if [ ! -f "$HOME/.@helproot/MiCommunityTool.py" ]; then
    echo -e "${RED}[✗] Download failed! Check internet connection.${RESET}"
    exit 1
fi

echo -e "${BLUE}[•] Creating launcher...${RESET}"

# Launcher command
cat > $PREFIX/bin/@helproot << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/.@helproot/MiCommunityTool.py "$@"
EOF

chmod +x $PREFIX/bin/@helproot

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗"
echo -e "║          ✅ INSTALL COMPLETE         ║"
echo -e "╚══════════════════════════════════════╝${RESET}"
echo -e "${WHITE}Made By: ${CYAN}@HelpRoot${RESET}"
echo -e "${YELLOW}Run tool using:${RESET} ${GREEN}@helproot${RESET}"
echo ""
