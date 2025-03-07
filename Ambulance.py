import paho.mqtt.client as mqtt
import time

# MQTT Configuration
MQTT_BROKER = "192.168.195.124"  
MQTT_PORT = 1883
MQTT_TOPIC_AMBULANCE = "emergency/ambulance"

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

def send_ambulance_signal(signal):
    mqtt_client.publish(MQTT_TOPIC_AMBULANCE, signal)
    print(f"Published signal: {signal}")

def main():
    try:
        while True:
            # Simulate ambulance arriving
            send_ambulance_signal("Ambulance Arriving")
            print("Ambulance signal sent. Waiting for 2 minutes...")
            time.sleep(60)  # Wait for 2 minutes
            
            
            # Simulate ambulance departing
            send_ambulance_signal("Ambulance Departed")
            print("Ambulance departed. Waiting for next cycle...")
            time.sleep(60)  # Wait before sending the next signal (optional)
    except KeyboardInterrupt:
        print("Ambulance program stopped.")
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()