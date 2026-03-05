#!/data/data/com.termux/files/usr/bin/bash

echo "Starting Wireless Observation Node..."

if ! command -v python >/dev/null; then
  echo "Python not installed. Run install.sh first."
  exit 1
fi

echo "Launching backend server..."

python app.py
