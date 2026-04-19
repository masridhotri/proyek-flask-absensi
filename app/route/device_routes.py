from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from app.model.device import device

device_bp = Blueprint('device', __name__)

@device_bp.route('/device/create', methods=['GET', 'POST'])
def create_progli():
    if request.method == 'POST':
        No_seri = request.form.get('No_seri')
        nama = request.form.get('nama')

        new_device = device(No_seri=No_seri, nama=nama)
        db.session.add(new_device)
        db.session.commit()

        return redirect(url_for('device.list_device'))

    return render_template('device/create.html')

@device_bp.route('/device')
def list_progli():
    data = device.query.all()
    return render_template('device/index.html', data=data)
@device_bp.route('/device/edit/<int:id>', methods=['GET', 'POST'])

def edit_progli(id):
    device = device.query.get_or_404(id)

    if request.method == 'POST':
        device.kode = request.form.get('kode')
        device.nama = request.form.get('nama')

        db.session.commit()
        return redirect(url_for('device.list_device'))

    return render_template('device/edit.html', device=device)
@device_bp.route('/device/delete/<int:id>')
def delete_device(id):
    device = device.query.get_or_404(id)

    db.session.delete(device)
    db.session.commit()

    return redirect(url_for('device.list_device'))