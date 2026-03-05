import time
import subprocess

start_time = time.time()
scan_count = 0


def get_cpu_usage():

    try:
        out = subprocess.check_output(
            ["top", "-n", "1"],
            text=True
        )

        for line in out.splitlines():
            if "CPU" in line:
                parts = line.split("%")
                return float(parts[0].split()[-1])

    except:
        return 0.0

    return 0.0


def get_memory_usage():

    try:
        out = subprocess.check_output(
            ["free", "-m"],
            text=True
        )

        lines = out.splitlines()
        mem = lines[1].split()

        used = mem[2]

        return int(used)

    except:
        return 0


def get_system_status():

    global scan_count
    scan_count += 1

    uptime = int(time.time() - start_time)

    return {
        "uptime": uptime,
        "scans": scan_count,
        "cpu": get_cpu_usage(),
        "memory_mb": get_memory_usage()
    }
