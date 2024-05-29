#!/bin/bash

current_date=$(date +'%Y-%m-%d')

subfolder_path="./webApp/photos/$current_date"
mkdir -p "$subfolder_path"

current_time=$(date +'%H%M%S')
milliseconds=$(date +'%N' | cut -b1-3)

photo_name="${current_time}_${milliseconds}.jpg"
photo_path="$subfolder_path/$photo_name"
rpicam-still -t 0.01 -o "$photo_path"
echo "Photo captured at $photo_path"

subject_distance=$(exiftool -SubjectDistance "$photo_path" | awk '{print $NF}')
subject_distance_float=$(echo "scale=2; $subject_distance / 1000" | bc)
exposure_time=$(exiftool -ExposureTime "$photo_path" | awk '{print $NF}')
ISO=$(exiftool -ISO "$photo_path" | awk '{print $NF}')

if [ "$1" == "motion" ]; then
    trigger="motion"
elif [ "$1" == "external" ]; then
    trigger="external"
else
    trigger="timer"
fi

sidecar_file="${photo_path%.jpg}.json"
cat << EOF > "$sidecar_file"
{
  "File Name": "$photo_name",
  "Create Date": "$(date +'%Y-%m-%d %H:%M:%S')$milliseconds+02:00",
  "Create Seconds Epoch": "$(date +'%s')$milliseconds",
  "Trigger": "$trigger",
  "Subject Distance": "$subject_distance",
  "Exposure Time": "$exposure_time",
  "ISO": "$ISO"
}
EOF
echo "Sidecar JSON file created successfully at $sidecar_file"

log_file="./webApp/logs/trigger_log.txt"
mkdir -p "$(dirname "$log_file")"
new_entry="$(date +'%Y-%m-%d %H:%M:%S') - Trigger: $trigger"
if [ -f "$log_file" ]; then
    (echo "$new_entry"; cat "$log_file") > "$log_file.tmp" && mv "$log_file.tmp" "$log_file"
else
    echo "$new_entry" > "$log_file"
fi
