import subprocess
import time
import logging
from datetime import datetime

# Configure logging for Docker (outputs to stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

TARGET_IP = "192.168.4.1"  # Replace with your UDM IP
CHECK_INTERVAL = 10        # Seconds between checks

def check_ping(ip):
    # -c 1: send 1 packet, -W 2: timeout after 2 seconds
    result = subprocess.run(
        ['ping', '-c', '1', '-W', '2', ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def main():
    logging.info(f"Starting Wi-Fi monitor tracking target: {TARGET_IP}")
    was_offline = False
    offline_start_time = None

    while True:
        is_online = check_ping(TARGET_IP)

        if not is_online and not was_offline:
            was_offline = True
            offline_start_time = datetime.now()
            logging.error(f"NETWORK DROP DETECTED. Target {TARGET_IP} is unreachable.")
        
        elif is_online and was_offline:
            downtime = datetime.now() - offline_start_time
            logging.info(f"CONNECTION RESTORED. Total downtime: {downtime}")
            was_offline = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
