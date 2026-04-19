from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from extensions import db
from app.model.data_progli import DataProgli

progli_bp = Blueprint('progli', __name__)

# ================= PAGE =================
@progli_bp.route('/progli')
def list_progli():
    return render_template('listprogli.html')


# ================= API =================



@progli_bp.route('/api/progli', methods=['POST'])
def api_create_progli():
    data = request.get_json()

    if not data:
        return {"error": "No data"}, 400

    progli = DataProgli(
        kode=data.get('kode'),
        nama=data.get('nama')
    )

    db.session.add(progli)
    db.session.commit()

    return {"status": "success"}


@progli_bp.route('/api/progli/<int:id>', methods=['PUT'])
def api_update_progli(id):
    data = request.get_json()
    progli = DataProgli.query.get_or_404(id)

    progli.kode = data.get('kode')
    progli.nama = data.get('nama')

    db.session.commit()
    return {"status": "updated"}


@progli_bp.route('/api/progli/<int:id>', methods=['DELETE'])
def api_delete_progli(id):
    progli = DataProgli.query.get_or_404(id)

    db.session.delete(progli)
    db.session.commit()

    return {"status": "deleted"}