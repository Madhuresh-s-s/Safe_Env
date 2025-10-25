import paho.mqtt.client as mqtt
import time

# MQTT Configuration
MQTT_BROKER = "10.88.15.124"  
MQTT_PORT = 1883
MQTT_TOPIC_SIGNBOARD = "road/signboard"

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

def send_signboard_alert():
    try:
        # Publish the signboard alert message
        mqtt_client.publish(MQTT_TOPIC_SIGNBOARD, "Signboard Alert")
        print("Published: Signboard Alert")
    except Exception as e:
        print(f"Failed to publish message: {e}")

def main():
    try:
        while True:
            # Simulate sending a signboard alert every 10 seconds
            send_signboard_alert()
            print("Waiting for 1 seconds before sending the next alert...")
            time.sleep(2)  # Wait for 10 seconds
    except KeyboardInterrupt:
        print("Signboard program stopped.")
    finally:
        # Clean up resources
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("MQTT client disconnected.")

if __name__ == "__main__":
    main()