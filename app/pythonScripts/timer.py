import subprocess
import time

def take_photo():
    subprocess.run(["take_photo.sh", "timer"])

if __name__ == "__main__":
    while True:
        take_photo()
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)
