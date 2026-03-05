import subprocess
import json

def scan_cells():

    try:

        result = subprocess.check_output(
            ["termux-telephony-cellinfo"]
        )

        cells = json.loads(result.decode())

        return cells

    except:
        return []
