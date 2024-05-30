#!/bin/bash

SSID="EMLI-TEAM-02"
PASSWORD="camera1234"
PI_USER="wildlife"
PI_IP="192.168.10.1"
PI_PICTURES_DIR="/home/wildlife/app/webApp/photos"
LOCAL_PICTURES_DIR="./photos"
DRONE_ID="WILDDRONE-001"
LOG_FILE="./sync_log.txt"
PI_PASSWORD="camera1234"

connect_to_wifi() {
    echo "Connecting to: $SSID"
    nmcli d wifi connect "$SSID" password "$PASSWORD"
    if [ $? -ne 0 ]; then
        echo "Failed to connect" | tee -a $LOG_FILE
        return 1
    fi
    echo "Connected successfully." | tee -a $LOG_FILE
    return 0
}

sync_time() {
    echo "Synchronizing time with the Raspberry Pi..."
    local current_time=$(date +%s)
    sshpass -p "$PI_PASSWORD" ssh -o StrictHostKeyChecking=no "$PI_USER@$PI_IP" "sudo date -s @$current_time"
    if [ $? -ne 0 ]; then
        echo "Failed to synchronize time." | tee -a $LOG_FILE
        return 1
    fi
    echo "Time synchronized successfully." | tee -a $LOG_FILE
    return 0
}

copy_files() {
    echo "Copying files from Raspberry Pi..."
    sshpass -p "$PI_PASSWORD" rsync -avz --ignore-existing "$PI_USER@$PI_IP:$PI_PICTURES_DIR/" "$LOCAL_PICTURES_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to copy files." | tee -a $LOG_FILE
        return 1
    fi
    echo "Files copied successfully." | tee -a $LOG_FILE
    return 0
}

update_json_files() {
    echo "Updating JSON files on the laptop..."
    find "$LOCAL_PICTURES_DIR" -type f -name '*.json' | while read json_file; do
        python3 - << EOPYTHON
import json
from time import time

file_path = "$json_file".strip()
if file_path:
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Add Drone Copy info only if it doesn't already exist
    if "Drone Copy" not in data:
        data["Drone Copy"] = {
            "Drone ID": "$DRONE_ID",
            "Seconds Epoch": time()
        }

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
EOPYTHON
    done
    if [ $? -ne 0 ]; then
        echo "Failed to update JSON files." | tee -a $LOG_FILE
        return 1
    fi
    echo "JSON files updated successfully." | tee -a $LOG_FILE
    return 0
}

echo "Script started at $(date)" | tee -a $LOG_FILE

connect_to_wifi
if [ $? -ne 0 ]; then
    echo "Error connecting to Wi-Fi." | tee -a $LOG_FILE
    exit 1
fi

sync_time
if [ $? -ne 0 ]; then
    echo "Error synchronizing time." | tee -a $LOG_FILE
    exit 1
fi

copy_files
if [ $? -ne 0 ]; then
    echo "Error copying files." | tee -a $LOG_FILE
    exit 1
fi

update_json_files
if [ $? -ne 0 ]; then
    echo "Error updating JSON files." | tee -a $LOG_FILE
    exit 1
fi

./annotate.sh "$LOCAL_PICTURES_DIR"
if [ $? -ne 0 ]; then
    echo "Error annotating pictures." | tee -a $LOG_FILE
    exit 1
fi

find "$LOCAL_PICTURES_DIR" -type f -name '*.json' | while read -r json_file; do
    if grep -q '"Annotation"' "$json_file"; then
        git add "$json_file"
    fi
done

git commit -m "Add annotations to JSON files"
git push git@github.com:OKThomsen/emli-02.git

echo "Script completed successfully at $(date)" | tee -a $LOG_FILE


