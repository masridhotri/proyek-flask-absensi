from flask import Blueprint, request
from datetime import datetime, timedelta
from extensions import db
from app.model.data_siswa import data_siswa
from app.model.absensi_siswa import absensi_siswa

sensor_bp = Blueprint('sensor', __name__)


# =========================
# REGISTER FINGER
# =========================
@sensor_bp.route('/scan/register', methods=['POST'])
def register_finger():
    data = request.get_json()
    finger_id = data.get('finger_id')

    if not finger_id:
        return {"status": "error", "message": "finger_id kosong"}, 400

    siswa = data_siswa.query.filter_by(finger_id=finger_id).first()
    if siswa:
        return {"status": "exists", "message": "Sudah terdaftar"}

    siswa = data_siswa(
        finger_id=finger_id,
        nama="Belum diisi",
        alamat="Belum diisi"
    )

    db.session.add(siswa)
    db.session.commit()

    return {"status": "success", "message": "Finger terdaftar"}


# =========================
# ABSENSI + ANTI DOUBLE
# =========================
@sensor_bp.route('/scan/absen', methods=['POST'])
def absen_finger():
    data = request.get_json()
    finger_id = data.get('finger_id')

    if not finger_id:
        return {"status": "error", "message": "finger_id kosong"}, 400

    siswa = data_siswa.query.filter_by(finger_id=finger_id).first()
    if not siswa:
        return {"status": "error", "message": "Tidak dikenal"}, 404

    # 🔥 Anti double scan (1 menit)
    last = (
        absensi_siswa.query
        .filter_by(siswa_id=siswa.id)
        .order_by(absensi_siswa.waktu.desc())
        .first()
    )

    now = datetime.utcnow()

    if last and (now - last.waktu) < timedelta(secconds=30):
        return {"status": "duplicate", "message": "Tunggu 30 detik"}

    # simpan absensi
    absen = absensi_siswa(siswa_id=siswa.id, status="hadir")
    db.session.add(absen)
    db.session.commit()

    return {"status": "success", "nama": siswa.nama}