Safe_Env
AI-Powered Real-Time Road Hazard Detection & Vehicle-to-Vehicle (V2V) Alert System

Project Logo
Enhancing urban road safety through AI-driven hazard detection and smart communication

Table of Contents
Features
Architecture
Getting Started
Usage
Dependencies
Contributing
License
Features
✅ Real-Time Hazard Detection :

Detects potholes, accidents, obstructions, weather risks, and traffic congestion using AI models (YOLOv8, CNN).
Dual data sources: Vehicle-mounted cameras and traffic cameras.
✅ Vehicle-to-Vehicle (V2V) Communication :

Broadcasts hazard alerts to nearby vehicles via DSRC/5G.
OpenXC or Car-to-X protocols for seamless integration.
✅ Roadside Viewboard Integration :

Displays real-time hazards on IoT-enabled boards at hotspots.
✅ Emergency Vehicle Priority :

Alerts traffic inspectors and drivers of approaching emergency vehicles.
Sends precise accident coordinates to emergency services via APIs.
✅ Collision Risk Mitigation :

Analyzes traffic camera feeds at junctions to prevent collisions.
Architecture
System Architecture

Data Collection :
Cameras (vehicle-mounted and traffic) stream video to edge devices.
AI Processing :
Pre-trained models (e.g., YOLOv8) run on Raspberry Pi/Arduino for real-time inference.
V2V Communication :
Hazards are broadcast to nearby vehicles via dedicated short-range communication (DSRC).
Viewboard Display :
Alerts pushed to IoT boards using MQTT/HTTP.
Emergency Response :
Accident coordinates sent to emergency APIs (e.g., Firebase, AWS IoT).
Getting Started
Prerequisites
Python 3.8+
Raspberry Pi 4 or similar edge device
Vehicle-mounted cameras (e.g., Raspberry Pi Camera Module)
Traffic cameras (IP cameras supported)
Setup
Clone the repository :
bash
Copy
1
git clone https://github.com/your-username/Safe_Env.git  
Install dependencies :
bash
Copy
1
pip install -r requirements.txt  
Configure hardware :
Connect cameras and set up camera feeds in config/camera_config.yaml.
Configure V2V communication settings in config/v2v_config.json.
Run the system :
bash
Copy
1
2
3
4
5
6
7
8
# Start AI inference (vehicle-mounted):  
python src/vehicle_ai.py  

# Start traffic camera monitoring:  
python src/traffic_monitor.py  

# Run V2V communication server:  
python src/v2v_server.py  
Usage
Hazard Detection :
The AI module processes video feeds and identifies hazards.
Alert Distribution :
V2V alerts are sent to nearby vehicles.
Viewboards update with real-time hazard data.
Emergency Response :
Accidents trigger automatic alerts to emergency services.
Dependencies
tensorflow-lite
On-device AI inference
opencv-python
Video feed processing
paho-mqtt
IoT communication for viewboards
flask
REST API for emergency services

Contributing
Fork the repo.
Create a branch: git checkout -b feature/<your-feature>.
Implement changes and test.
Submit a PR with clear documentation.
Areas to contribute :

Optimize AI model efficiency.
Improve V2V communication protocols.
Enhance viewboard IoT integration.
License
This project is licensed under the MIT License — see the LICENSE file.

Acknowledgments
Open-source tools: TensorFlow Lite, OpenCV, MQTT.
Inspired by NHTSA safety guidelines and IEEE smart city research.
