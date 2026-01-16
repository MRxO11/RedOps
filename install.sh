#!/bin/bash
set -e

echo
echo "======================================"
echo "        RedOps Full Installer"
echo "======================================"
echo

# ============ ROOT CHECK ============
if [[ "$EUID" -ne 0 ]]; then
  echo "[!] Run as root:"
  echo "    sudo ./install.sh"
  exit 1
fi

# ============ UPDATE SYSTEM ============
echo "[*] Updating system..."
apt update -y

# ============ CORE PACKAGES ============
echo "[*] Installing core system tools..."
apt install -y \
  git curl wget unzip build-essential \
  python3 python3-pip python3-venv pipx \
  nmap nikto whatweb smbclient ldap-utils \
  exploitdb netcat-openbsd

pipx ensurepath

# ============ METASPLOIT ============
echo "[*] Installing Metasploit Framework..."
if ! command -v msfconsole &> /dev/null; then
  curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb -o msfinstall
  chmod +x msfinstall
  ./msfinstall
  rm -f msfinstall
else
  echo "  → Metasploit already installed"
fi

# ============ NUCLEI ============
echo "[*] Installing Nuclei..."
if ! command -v nuclei &> /dev/null; then
  wget https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei-linux-amd64.zip
  unzip nuclei-linux-amd64.zip
  mv nuclei /usr/local/bin/
  chmod +x /usr/local/bin/nuclei
  rm -f nuclei-linux-amd64.zip
else
  echo "  → Nuclei already installed"
fi

echo "[*] Updating nuclei templates..."
nuclei -update-templates || true

# ============ PYTHON LIBS ============
echo "[*] Installing Python libraries..."
pip3 install --upgrade pip
pip3 install textual rich async-timeout

# ============ ADE INSTALL ============
echo
echo "[*] Installing ADE into tools/ade"

ADE_PATH="tools/ade"

if [ -d "$ADE_PATH" ]; then
  echo "  → Existing ADE found, removing..."
  rm -rf "$ADE_PATH"
fi

mkdir -p tools
cd tools

git clone https://github.com/blue-pho3nix/ade.git ade
cd ade

apt install -y git pipx
pipx ensurepath
chmod +x install.sh
./install.sh

cd ../../

# ============ FINISHED ============
echo
echo "======================================"
echo "   RedOps installation completed"
echo
echo "   Launch with:"
echo "      python3 main.py"
echo "======================================"
echo
