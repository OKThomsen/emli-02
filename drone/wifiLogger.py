import sqlite3
import time
import subprocess
import re
import os

def get_wifi_stats():
    with open('/proc/net/wireless', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'wlp5s0' in line:  # Replace 'wlan0' with your wireless interface name
                data = line.split()
                link_quality = int(data[2].split('.')[0])
                signal_level = int(data[3].split('.')[0])
                print(f"Link Quality: {link_quality}, Signal Level: {signal_level}")  # Debug print
                return link_quality, signal_level
    return None, None


def get_current_ssid():
    try:
        ssid = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
        return ssid
    except subprocess.CalledProcessError:
        return None

def log_to_db(db_path, timestamp, link_quality, signal_level):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, link_quality, signal_level) VALUES (?, ?, ?)", (timestamp, link_quality, signal_level))
    conn.commit()
    conn.close()

def setup_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        timestamp INTEGER,
        link_quality INTEGER,
        signal_level INTEGER
    )
    """)
    conn.commit()
    conn.close()

def main():
    # Specify the directory and database name
    db_directory = "./WiFiLog"  # Replace with your desired directory
    db_name = "wifi_log.db"
    db_path = os.path.join(db_directory, db_name)

    # Create the directory if it doesn't exist
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    # Set up the database and table
    setup_database(db_path)

    pattern = re.compile(r"EMLI-TEAM-02")  # Regex pattern to match "EMLI-TEAM-XX"
    while True:
        current_ssid = get_current_ssid()
        if current_ssid and pattern.match(current_ssid):
            timestamp = int(time.time())
            link_quality, signal_level = get_wifi_stats()
            if link_quality is not None and signal_level is not None:
                log_to_db(db_path, timestamp, link_quality, signal_level)
        time.sleep(10)  # Adjust the sleep interval as needed

if __name__ == "__main__":
    main()
