import paho.mqtt.client as mqtt
import json
import time
import queue
import threading
from gtts import gTTS     
import pygame             
import os                 

MQTT_BROKER = "10.88.15.124"  
MQTT_PORT = 1883
TOPIC_ACCIDENT = "detection/accident"
TOPIC_POTHOLE = "detection/pothole_speedbump"
TOPIC_PRIORITY = "traffic/priority_route"

speech_queue = queue.Queue()
AUDIO_FILE = "alert.mp3"  


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker at {MQTT_BROKER}.")
    client.subscribe(TOPIC_ACCIDENT)
    client.subscribe(TOPIC_POTHOLE)
    client.subscribe(TOPIC_PRIORITY)
    print(f"Subscribed to: {TOPIC_ACCIDENT}, {TOPIC_POTHOLE}, {TOPIC_PRIORITY}")
    speech_queue.put("Voice assistant connected and ready.")

def on_message(client, userdata, message):
    """
    This function is called in the MQTT thread.
    It just adds messages to the queue.
    """
    topic = message.topic
    try:
        payload_str = message.payload.decode("utf-8")
        
        if topic == TOPIC_POTHOLE:
            data = json.loads(payload_str)
            hazard_type = data.get("hazard", "hazard")
            speech_queue.put(f"{hazard_type} detected ahead.")
            
        elif topic == TOPIC_ACCIDENT:
            data = json.loads(payload_str)
            location_name = data.get("location_data", {}).get("name", "an unknown location")
            speech_queue.put(f"Warning: Accident reported at {location_name}.")
            
        elif topic == TOPIC_PRIORITY:
            speech_queue.put(payload_str)
            
    except Exception as e:
        print(f"Error in on_message: {e}")


def speech_worker():
    """
    This function runs in a dedicated thread.
    It waits for messages, creates an MP3, and plays it using pygame.
    """
    print("Speech worker thread started.")
    pygame.mixer.init()  
    
    while True:
        try:
            text_to_say = speech_queue.get()
            
            print(f"VOICE_ASSISTANT: Speaking: '{text_to_say}'")
            
            tts = gTTS(text=text_to_say, lang='en')
            
            tts.save(AUDIO_FILE)
            
            pygame.mixer.music.load(AUDIO_FILE)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload() 
            
            os.remove(AUDIO_FILE)
            
            speech_queue.task_done() 
            
        except Exception as e:
            print(f"Error in speech worker: {e}")
            try:
                pygame.mixer.music.unload()
                if os.path.exists(AUDIO_FILE):
                    os.remove(AUDIO_FILE)
            except Exception as e2:
                print(f"Error during cleanup: {e2}")

if __name__ == "__main__":
    speech_thread = threading.Thread(target=speech_worker, daemon=True)
    speech_thread.start()

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    print(f"Connecting to MQTT broker at {MQTT_BROKER}...")
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        exit()

    mqtt_client.loop_start()

    print("Voice assistant is running. Press CTRL+C to exit.")
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        mqtt_client.loop_stop()
        print("Disconnected from MQTT.")
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)