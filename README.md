# Wireless Observatory Node

A lightweight **RF and wireless monitoring dashboard** designed to run directly on Android using **Termux**.

The system scans wireless activity and visualizes data in a browser dashboard with radar visualization, spectrum metrics, device detection, and sensor information.

This project is designed as a **portable wireless monitoring node** that can run entirely on a mobile device.

---

## First Time Installation (Run Once)

## First install Termux and Termux API from FDroid
## Then give Termux API Location access

## If Play Protect prevents Termux API from installing, disable it from Play Store.

Run this single command in Termux:

```bash
pkg install git -y
git clone https://github.com/My-Mation/network-scanner
cd network-scanner
chmod +x install.sh
./install.sh
./start.sh

```
Stop it by clicking Ctrl C

```bash
cd ~/network-scanner
./start.sh

```
## Features

- Real-time RF activity dashboard
- Radar visualization of detected signals
- WiFi network scanning
- RF signal metrics and channel spectrum
- Device presence monitoring
- RF density graph
- Motion detection
- Device sensor integration
- Automated setup using install script

---

## Dashboard Components

The dashboard includes several monitoring panels:

- RF Radar visualization
- RF Metrics
- Channel Spectrum
- WiFi Networks Table
- Device Presence Panel
- RF Density Graph
- Motion Detection Panel
- Device Sensors Panel
- Alerts Panel

The interface uses a **dark cyber-console style UI** designed for continuous monitoring.

---

## Requirements

Android device with:

- **Termux**
- **Termux:API app installed**
- WiFi hardware capable of scanning

Some Android devices restrict wireless scanning capabilities.

---

## Project Structure

```
wireless-observatory/
│
├── app.py          # Flask backend server
├── scanner.py      # Wireless scanning logic
├── install.sh      # Automated setup script
├── start.sh        # Starts the monitoring node
├── README.md       # Documentation
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── radar.js
```

---

## Technologies Used

- Python
- Flask
- JavaScript
- HTML / CSS
- Termux API
- Linux wireless tools

---

## Disclaimer

This project is intended for **educational and research purposes only**.

Wireless monitoring features depend on device hardware and Android restrictions.

---

## License

MIT License
