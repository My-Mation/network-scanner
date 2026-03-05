from scanner.security_analyzer import classify_security
from scanner.vendor_lookup import get_vendor
import subprocess
import json

def frequency_to_channel(freq):

    if 2412 <= freq <= 2472:
        return int((freq - 2407) / 5)

    if 5000 <= freq <= 5895:
        return int((freq - 5000) / 5)

    return None


def band_from_freq(freq):

    if freq < 3000:
        return "2.4GHz"
    else:
        return "5GHz"


def scan_wifi():

    networks = []

    result = subprocess.check_output(["termux-wifi-scaninfo"])
    data = json.loads(result.decode())

    for net in data:

        freq = net["frequency_mhz"]

        networks.append({
            "ssid": net["ssid"],
            "bssid": net["bssid"],
            "vendor": get_vendor(net["bssid"]),
            "rssi": net["rssi"],
            "frequency": freq,
            "channel": frequency_to_channel(freq),
            "band": band_from_freq(freq),
            "security": net["capabilities"]
        })

    return networks
