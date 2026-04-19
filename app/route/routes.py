from flask import render_template, jsonify, request, redirect
from models import SensorData
from extensions import db

from app.model.data_progli import DataProgli
from app.model.data_siswa import data_siswa



def register_routes(app):

    @app.route('/')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/create')
    def create_page():
        return render_template('Create.html')

    @app.route('/list')
    def listdata():
        return render_template('listdata.html')

    @app.route('/device')
    def device():
        return render_template('listdevice.html')

    @app.route('/progli')
    def progli():
        return render_template('listprogli.html')
    @app.route('/finger')
    def finger():
        return render_template('listfinger.html')

    # ================= API PROGLI =================

    @app.route('/api/progli', methods=['GET'])
    def api_get_progli():
        data = DataProgli.query.all()

        return jsonify([
          {
                "id": d.id,
                "kode": d.kode,
                "nama": d.nama
            }
        for d in data
    ])

    @app.route('/progli/create', methods=['POST'])
    def create_progli():
        kode = request.form.get('kode')
        nama = request.form.get('nama')

        progli = DataProgli(kode=kode, nama=nama)

        db.session.add(progli)
        db.session.commit()

        return redirect('/progli')
    @app.route('/api/progli/<int:id>', methods=['DELETE'])
    def delete_progli(id):
         data = DataProgli.query.get_or_404(id)

         db.session.delete(data)
         db.session.commit()

         return jsonify({"status": "deleted"})

# =================== Data Siswa =============

    @app.route('/api/siswa/daftar', methods=['POST'])
    def daftar_siswa():
        data = request.get_json()

        finger_id = data.get('finger_id')

        if finger_id is None:
            return jsonify({"status": "error", "message": "finger_id kosong"}), 400

    # cek sudah ada atau belum
        existing = data_siswa.query.filter_by(finger_id=finger_id).first()

        if existing:
            return jsonify({
                "status": "exist",
                "message": "finger_id sudah terdaftar"
         })

    # CREATE DATA BARU
        siswa = data_siswa(
            finger_id=finger_id
        )

        db.session.add(siswa)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "siswa berhasil didaftarkan",
            "finger_id": finger_id
        })

# =================== finger =============
    @app.route('/api/siswa/daftar-list', methods=['GET'])
    def list_siswa_belum_lengkap():
     data = data_siswa.query.all()

     hasil = []

     for s in data:
        # ❌ skip kalau sudah lengkap
        if s.nama is not None and s.kelas is not None:
            continue

        hasil.append({
            "id": s.id,
            "finger_id": s.finger_id,
            "nama": s.nama,
            "kelas": s.kelas,
            "nisn": s.nisn,
            "email": s.email,
            "alamat": s.alamat,
            "no_tlp": s.no_tlp
        })

     return jsonify(hasil)



    # ================= SENSOR =================

    @app.route('/api/data', methods=['GET'])
    def get_data():
        data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(20).all()

        return jsonify([
            {
                "sensor_name": d.sensor_name,
                "value": d.value,
                "timestamp": d.timestamp.isoformat()
            }
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