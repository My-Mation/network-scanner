import sqlite3

def detect_movement(bssid, new_rssi):

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT rssi FROM wifi_scans WHERE bssid=? ORDER BY timestamp DESC LIMIT 1",
        (bssid,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return "new"

    old_rssi = row[0]

    delta = new_rssi - old_rssi

    if delta > 8:
        return "approaching"

    if delta < -8:
        return "leaving"

    return "stable"
