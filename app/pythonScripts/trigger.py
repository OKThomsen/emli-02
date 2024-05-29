import paho.mqtt.client as mqtt
import os
import subprocess

# MQTT settings
MQTT_BROKER = "192.168.10.1"
MQTT_PORT = 1883
MQTT_TOPIC = "test"

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    print(f"Message received: {message.payload.decode()}")
    
    if message.payload.decode() == "Button pressed":
        print("Running take_photo.sh script...")
        result = subprocess.run(["./take_photo.sh", "external"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Script executed successfully")
        else:
            print("Script execution failed", result.stderr)

# Initialize MQTT client and connect to the broker
client = mqtt.Client()
client.on_message = on_message

print("Connecting to MQTT broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)

# Start the loop to process received messages
client.loop_forever()
import subprocess

def main():
    subprocess.run(['./take_photo.sh', 'external'])

if __name__ == "__main__":
    main()
