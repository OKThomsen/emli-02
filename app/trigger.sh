#!/bin/bash

MQTT_BROKER="192.168.10.1"
MQTT_PORT=1883
MQTT_TOPIC="test"

on_message() {
    echo "Message received: $1"
    if [ "$1" = "Button pressed" ]; then
        echo "Running take_photo.sh script..."
        if ./take_photo.sh external; then
            echo "Script executed successfully"
        else
            echo "Script execution failed"
        fi
    fi
}

echo "Connecting to MQTT broker..."
mosquitto_sub -h "$MQTT_BROKER" -p "$MQTT_PORT" -t "$MQTT_TOPIC" | while read -r message; do
    on_message "$message"
done
