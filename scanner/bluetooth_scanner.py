import subprocess
import json

def scan_bluetooth():

    try:
        result = subprocess.check_output(["termux-bluetooth-scan"])
        return json.loads(result.decode())

    except:
        return []
