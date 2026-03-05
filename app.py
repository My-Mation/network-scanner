from analytics.presence_tracker import update_presence
from analytics.motion_analysis import analyze_motion
from analytics.density_timeline import update_density_timeline
from analytics.system_status import get_system_status
from scanner.cell_scanner import scan_cells
from scanner.sensor_scanner import scan_sensors
from scanner.anomaly_detector import detect_changes
from analytics.density import rf_density
from scanner.device_classifier import classify_device
from scanner.movement import detect_movement
from database.store_scan import store_wifi
from scanner.network_scanner import scan_network
from scanner.vendor_lookup import load_vendors
from flask import Flask, render_template, jsonify
from scanner.wifi_scanner import scan_wifi
import time

app = Flask(__name__)
load_vendors()

start_time = time.time()


def analyze_channels(networks):

    channels = {}

    for net in networks:

        ch = net["channel"]

        if ch not in channels:
            channels[ch] = 0

        channels[ch] += 1

    return channels


def vendor_stats(networks):

    vendors = {}

    for net in networks:

        v = net.get("vendor") or "Unknown"

        if v not in vendors:
            vendors[v] = 0

        vendors[v] += 1

    return vendors


def signal_histogram(networks):

    bins = {
        "-30":0,"-40":0,"-50":0,
        "-60":0,"-70":0,"-80":0,"-90":0
    }

    for net in networks:

        r = net.get("rssi")

        if r is None:
            continue

        if r >= -30:
            bins["-30"] += 1
        elif r >= -40:
            bins["-40"] += 1
        elif r >= -50:
            bins["-50"] += 1
        elif r >= -60:
            bins["-60"] += 1
        elif r >= -70:
            bins["-70"] += 1
        elif r >= -80:
            bins["-80"] += 1
        else:
            bins["-90"] += 1

    return bins


def rf_activity(networks):

    hidden = 0
    hotspots = 0

    for n in networks:

        ssid = n.get("ssid")

        if not ssid:
            hidden += 1

        if ssid and "jio" in ssid.lower():
            hotspots += 1

    return {
        "total_networks": len(networks),
        "hidden_networks": hidden,
        "hotspots": hotspots
    }


def security_summary(networks):

    open_nets = 0

    for n in networks:

        cap = n.get("security")

        if cap == "Open":
            open_nets += 1

    return {
        "open_networks": open_nets
    }


def environment_summary(networks, density):

    if density < 300:
        level = "Low density"
    elif density < 700:
        level = "Moderate density"
    elif density < 1000:
        level = "High density"
    else:
        level = "Extreme RF congestion"

    return {
        "environment": level,
        "network_count": len(networks)
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan")
def scan():

    scan_start = time.time()

    wifi = scan_wifi()

    for net in wifi:
        net["movement"] = detect_movement(net["bssid"], net["rssi"])
        net["device_type"] = classify_device(net["vendor"], net["ssid"])

    lan = ""
    cells = scan_cells()
    sensors = scan_sensors()

    channels = analyze_channels(wifi)

    changes = detect_changes(wifi)

    uptime = int(time.time() - start_time)

    density = rf_density(wifi)

    store_wifi(wifi)

    system_status = get_system_status()

    scan_time = round((time.time() - scan_start) * 1000, 1)

    vendors = vendor_stats(wifi)
    histogram = signal_histogram(wifi)
    activity = rf_activity(wifi)
    security = security_summary(wifi)
    environment = environment_summary(wifi, density)

    presence = update_presence(wifi)
    motion = analyze_motion(wifi)
    density_timeline = update_density_timeline(density)

    events = [
        f"{len(wifi)} WiFi networks detected",
        f"{len(cells)} cell towers visible",
        f"RF density score {density}"
    ]

    return jsonify({
        "wifi": wifi,
        "channels": channels,
        "uptime": uptime,
        "density": density,
        "changes": changes,
        "lan": lan,
	"presence": presence,
	"motion": motion,
	"density_timeline": density_timeline,
        "cells": cells,
        "system": system_status,
        "sensors": sensors,

        "rf_activity": activity,
        "histogram": histogram,
        "vendors": vendors,
        "scan_time": scan_time,
        "events": events,
        "security": security,
        "environment": environment
    })


@app.route("/history/<bssid>")
def history(bssid):

    import sqlite3

    conn = sqlite3.connect("database/db.sqlite3")
    cur = conn.cursor()

    cur.execute(
        "SELECT timestamp,rssi FROM wifi_scans WHERE bssid=? ORDER BY timestamp DESC LIMIT 100",
        (bssid,)
    )

    rows = cur.fetchall()

    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
