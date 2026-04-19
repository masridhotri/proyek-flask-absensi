from flask import Flask
from config import Config
from extensions import db, migrate
from app.route.progli_routes import progli_bp
from app.route.device_routes import device_bp
from app.route.sensor_routes import sensor_bp
from app.route.data_siswa import siswa_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(app.url_map)

    db.init_app(app)
    migrate.init_app(app, db)

    # load semua model
    from app import model

    # register blueprint
    app.register_blueprint(progli_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(siswa_bp)

    return app