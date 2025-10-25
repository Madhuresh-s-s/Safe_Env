import paho.mqtt.client as mqtt
import json
import time

# Configuration
MQTT_BROKER = "10.88.15.124"  # Must be the same as your car
MQTT_PORT = 1883
AMBULANCE_ID = "Ambulance_007"

# Topics
ACCIDENT_TOPIC = "detection/accident"
RESPONSE_TOPIC = "ambulance/response"
ARRIVAL_TOPIC = "emergency/ambulance" # To tell the car script

# Callback for when we get an accident message
def on_message(client, userdata, message):
    if message.topic == ACCIDENT_TOPIC:
        print("\n--- NEW ACCIDENT RECEIVED ---")
        
        # 1. Decode the message
        data = json.loads(message.payload.decode("utf-8"))
        location_name = data['location_data']['name']
        print(f"Location: {location_name}")
        
        # 2. Simulate "Accepting" the request
        print("Simulating review... accepting in 5 seconds.")
        time.sleep(5)
        
        response_payload = {
            "ambulance_id": AMBULANCE_ID,
            "status": "Accepted",
            "location_name": location_name,
            "vehicle_id": data['vehicle_id']
        }
        client.publish(RESPONSE_TOPIC, json.dumps(response_payload))
        print(f"Published ACCEPTANCE to {RESPONSE_TOPIC}")

        # 3. Simulate "Arriving" at the scene
        print("Simulating travel... arriving in 10 seconds.")
        time.sleep(10)
        
        # This is the message your original car script is listening for
        client.publish(ARRIVAL_TOPIC, "Ambulance Arriving")
        print(f"Published ARRIVAL to {ARRIVAL_TOPIC}\n")

# --- Standard MQTT Setup ---
def on_connect(client, userdata, flags, rc):
    print("Ambulance Simulator Connected to MQTT.")
    client.subscribe(ACCIDENT_TOPIC)
    print(f"Subscribed to {ACCIDENT_TOPIC}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_forever()