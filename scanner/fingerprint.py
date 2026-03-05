def create_fingerprint(networks):

    fp = set()

    for net in networks:
        fp.add(net["bssid"])

    return fp
