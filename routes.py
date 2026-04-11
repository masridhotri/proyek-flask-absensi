from flask import render_template, jsonify, request
from app import app, db
from models import SensorData

@app.route('/')
def dashboard():
    return render_template('dashboard.html')
@app.route('/create')
def create():
    return render_template('Create.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(20).all()
    return jsonify([
        {"sensor_name": d.sensor_name, "value": d.value, "timestamp": d.timestamp.isoformat()} 
        for d in data
    ])

@app.route('/api/data', methods=['POST'])
def add_data():
    json_data = request.get_json()
    new_data = SensorData(
        sensor_name=json_data['sensor_name'],
        value=json_data['value']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"status": "success"})