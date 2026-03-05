#!/data/data/com.termux/files/usr/bin/bash

echo "====================================="
echo "Wireless Observatory Installer"
echo "====================================="

echo "Updating Termux..."
pkg update -y
pkg upgrade -y

echo "Installing core packages..."
pkg install -y \
python \
git \
nodejs \
termux-api \
iw \
net-tools \
nmap

echo "Installing Python dependencies..."
pip install --upgrade pip

pip install \
flask \
flask-cors \
requests

echo "Checking Termux API..."

if command -v termux-wifi-scaninfo >/dev/null 2>&1
then
echo "Termux API detected."
else
echo "WARNING:"
echo "Install the Termux:API Android app from:"
echo "https://f-droid.org/packages/com.termux.api/"
fi

echo ""
echo "Setup finished."
echo "Run the system with:"
echo "./start.sh"
