def classify_device(vendor, ssid):

    if "TP-Link" in vendor or "D-Link" in vendor:
        return "Router"

    if "Apple" in vendor or "Samsung" in vendor:
        return "Phone"

    if "Espressif" in vendor:
        return "IoT"

    if "OPPO" in ssid:
        return "Phone hotspot"

    return "Unknown"
