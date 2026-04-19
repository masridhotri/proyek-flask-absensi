from flask import Flask
from config import Config
from extensions import db
from app.route.routes import register_routes

import threading
from controller import start_mqtt


app = Flask(__name__)
app.config.from_object(Config)

# ================= DB INIT =================
db.init_app(app)

# ================= ROUTES =================
register_routes(app)

# ================= CONTEXT INIT =================
with app.app_context():
    db.create_all()


# ================= BACKGROUND SERVICES =================
def run_mqtt():
    start_mqtt()


# ================= MAIN =================
if __name__ == "__main__":

    mqtt_thread = threading.Thread(
        target=run_mqtt,
        daemon=True
    )
    mqtt_thread.start()

    app.run(
        debug=True,
        port=3360
    )