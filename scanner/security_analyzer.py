def classify_security(capabilities):

    if "WPA3" in capabilities:
        return "WPA3"

    if "WPA2" in capabilities:
        return "WPA2"

    if "WEP" in capabilities:
        return "WEP (insecure)"

    return "OPEN"
