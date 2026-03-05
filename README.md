# Wireless Observatory Node

A lightweight **RF and wireless monitoring dashboard** designed to run directly on Android using **Termux**.

The system scans wireless activity and visualizes data in a browser dashboard with radar visualization, spectrum metrics, device detection, and sensor information.

This project is designed as a **portable wireless monitoring node** that can run entirely on a mobile device.

---

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

## Installation

Clone the repository:

```bash
pkg install git
git clone https://github.com/YOUR_USERNAME/wireless-observatory
cd wireless-observatory
```

Run the installer:

```bash
chmod +x install.sh
./install.sh
```

Start the node:

```bash
./start.sh
```

---

## Access the Dashboard

Open your browser and navigate to:

```
http://localhost:5000
```

The wireless monitoring dashboard will load.

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
