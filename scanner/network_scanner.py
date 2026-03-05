import subprocess

def scan_network():

    try:

        result = subprocess.check_output(
            ["nmap","-sn","192.168.1.0/24"]
        )

        return result.decode()

    except:
        return ""
