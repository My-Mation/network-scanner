vendors = {}

def load_vendors():

    with open("data/oui.txt") as f:

        for line in f:

            if "(hex)" in line:

                parts = line.split("(hex)")

                prefix = parts[0].strip().replace("-", ":")

                vendor = parts[1].strip()

                vendors[prefix] = vendor


def get_vendor(mac):

    prefix = mac[:8].upper()

    return vendors.get(prefix, "Unknown")
