import time

presence_db = {}

def update_presence(networks):
    now = time.time()

    for n in networks:
        bssid = n.get("bssid")
        if not bssid:
            continue

        if bssid not in presence_db:
            presence_db[bssid] = {
                "first_seen": now,
                "last_seen": now
            }
        else:
            presence_db[bssid]["last_seen"] = now

    result = []

    for bssid, data in presence_db.items():
        duration = int(data["last_seen"] - data["first_seen"])

        result.append({
            "bssid": bssid,
            "duration": duration
        })

    return result

