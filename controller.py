import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.18.129"
TOPIC = "esp/sensor"

def on_connect(client, userdata, flags, rc):
    print("MQTT CONNECTED")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"RAW: {payload}")

    try:
        data = json.loads(payload)
        handle_data(data)
    except Exception as e:
        print("ERROR PARSE:", e)

def handle_data(data):
    mode = data.get("mode")
    sensor_id = data.get("id")

    if mode == "register":
        print(f"[REGISTER] ID {sensor_id}")

    elif mode == "absent":
        print(f"[ABSEN] ID {sensor_id}")

    else:
        print("[UNKNOWN MODE]", data)

def start_mqtt():
    client = mqtt.Client("flask_listener")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()