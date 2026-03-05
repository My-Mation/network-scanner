def rf_density(networks):

    if not networks:
        return 0

    strength = 0

    for net in networks:
        strength += abs(net["rssi"])

    return len(networks) * (strength / len(networks))
