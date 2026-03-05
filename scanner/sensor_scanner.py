import subprocess
import json

def scan_sensors():

    try:

        result = subprocess.check_output([
            "termux-sensor",
            "-a",
            "-n",
            "1"
        ])

        return json.loads(result.decode())

    except:
        return {}
