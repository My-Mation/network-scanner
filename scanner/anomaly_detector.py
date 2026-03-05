previous_devices = set()

def detect_changes(networks):

    global previous_devices

    current = set(net["bssid"] for net in networks)

    new_devices = current - previous_devices
    disappeared = previous_devices - current

    previous_devices = current

    return {
        "new": list(new_devices),
        "gone": list(disappeared)
    }
