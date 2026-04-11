from flask import Flask
from config import Config
import pymysql
import paho.mqtt.client as mqtt

from mqtt_cnf import *

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Config)

# =========================
# MQTT CALLBACK
# =========================
def on_message(client, userdata, msg):
    print(f"[MQTT] {msg.topic} -> {msg.payload.decode()}")

# =========================
# MQTT SETUP
# =========================
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
mqtt_client.subscribe(MQTT_TOPIC)

mqtt_client.loop_start()

# =========================
# ROUTE TEST
# =========================
@app.route("/")
def home():
    return "Flask + MQTT Running 🚀"

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)