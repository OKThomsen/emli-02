import serial
import json
import paho.mqtt.client as mqtt
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_PUBLISH_TOPIC = 'pico/data'
MQTT_SUBSCRIBE_TOPIC = 'pico/commands'

def open_serial_connection():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to serial port {SERIAL_PORT}")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

ser = open_serial_connection()

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_SUBSCRIBE_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print("Message received from MQTT: " + msg.payload.decode())
    try:
        data = json.loads(msg.payload.decode())
        if ser and ser.is_open:
            ser.write((json.dumps(data) + '\n').encode())
        else:
            print("Serial port not available")
    except json.JSONDecodeError:
        print("Failed to decode JSON from MQTT message")

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode().strip()
                if line:
                    data = json.loads(line)
                    print("Data received from Pico: ", data)
                    
                    client.publish(MQTT_PUBLISH_TOPIC, json.dumps(data))
                        
            except serial.SerialException as e:
                print(f"SerialException: {e}")
                ser.close()
                ser = open_serial_connection()
            except json.JSONDecodeError:
                print("Failed to decode JSON from serial data")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")

if ser:
    ser.close()
client.loop_stop()
client.disconnect()
