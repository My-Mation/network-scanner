import time

prev_rssi = {}
prev_time = {}

def analyze_motion(networks):
    now = time.time()
    output = []

    for n in networks:
        bssid = n.get("bssid")
        rssi = n.get("rssi")

        if not bssid or rssi is None:
            continue

        if bssid in prev_rssi:
            dt = now - prev_time[bssid]

            if dt > 0:
                velocity = (rssi - prev_rssi[bssid]) / dt
            else:
                velocity = 0
        else:
            velocity = 0

        prev_rssi[bssid] = rssi
        prev_time[bssid] = now

        output.append({
            "bssid": bssid,
            "velocity": round(velocity,2)
        })

    return output
