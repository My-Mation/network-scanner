import sqlite3
import time

def store_wifi(networks):

    conn = sqlite3.connect("database/db.sqlite3")

    cursor = conn.cursor()

    now = int(time.time())

    for net in networks:

        cursor.execute(
            "INSERT INTO wifi_scans (bssid, ssid, rssi, timestamp) VALUES (?,?,?,?)",
            (net["bssid"], net["ssid"], net["rssi"], now)
        )

    conn.commit()

    conn.close()
