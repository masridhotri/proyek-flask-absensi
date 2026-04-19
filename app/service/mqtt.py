import paho.mqtt.client as mqtt

def start_mqtt():

    def on_message(client, userdata, msg):
        print("DATA:", msg.payload.decode())

    client = mqtt.Client()
    client.on_message = on_message

    client.connect("localhost", 1883, 60)
    client.subscribe("sensor/data")
    client.loop_start()