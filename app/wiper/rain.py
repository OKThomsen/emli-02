import json
import paho.mqtt.client as mqtt
import time

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_DATA_TOPIC = 'pico/data'
MQTT_COMMAND_TOPIC = 'pico/commands'

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_DATA_TOPIC)
    else:
        print(f"Failed to connect")

def on_message(client, userdata, msg):
    print("Data received from MQTT: " + msg.payload.decode())
    try:
        data = json.loads(msg.payload.decode())
        if 'rain_detect' in data and data['rain_detect'] == 1:
            print("Rain detected!")
            commands = [{"wiper_angle": 180}, {"wiper_angle": 0}]
            for command in commands:
                client.publish(MQTT_COMMAND_TOPIC, json.dumps(command))
                time.sleep(5)
    except json.JSONDecodeError:
        print("Failed to decode JSON from MQTT message")

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()
