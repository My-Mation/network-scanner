#!/data/data/com.termux/files/usr/bin/bash

echo "====================================="
echo "Wireless Observatory Installer"
echo "====================================="

# Detect Termux
if [ ! -d "/data/data/com.termux/files" ]; then
  echo "This installer only works inside Termux."
  exit 1
fi

echo "Updating Termux packages..."
pkg update -y
pkg upgrade -y

echo "Installing required packages..."

pkg install -y python
pkg install -y git
pkg install -y nodejs
pkg install -y termux-api
pkg install -y net-tools
pkg install -y nmap

echo "Installing Python dependencies..."

python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ""
echo "Checking Termux API..."

if command -v termux-wifi-scaninfo >/dev/null 2>&1
then
  echo "Termux API detected."
else
  echo ""
  echo "WARNING:"
  echo "Install Termux:API Android app:"
  echo "https://f-droid.org/packages/com.termux.api/"
fi

echo ""
echo "IMPORTANT:"
echo "Enable LOCATION permission for the Termux:API app."
echo "Otherwise WiFi scanning will return empty results."

echo ""
echo "Setup complete."
echo "Run the system with:"
echo "./start.sh"
