// Embedded Linux (EMLI)
// University of Southern Denmark

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "EMLI-TEAM-02";
const char* password = "camera1234";

// MQTT server settings
const char* mqtt_server = "192.168.10.1";
const int mqtt_port = 1883;
const char* mqtt_topic = "test";

const int buttonPin = 4;  // GPIO 4 for the button
bool buttonPressed = false;

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  pinMode(buttonPin, INPUT_PULLUP);  // Configure the button pin as input with internal pull-up resistor
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  if (buttonState == LOW && !buttonPressed) {  // Button pressed (active low)
    buttonPressed = true;
    Serial.println("Button pressed, sending payload...");

    if (client.publish(mqtt_topic, "Button pressed")) {
      Serial.println("Message published successfully");
    } else {
      Serial.println("Message publishing failed");
    }
  } else if (buttonState == HIGH && buttonPressed) {  // Button released
    buttonPressed = false;
  }

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  delay(100);  // Debounce delay
}
