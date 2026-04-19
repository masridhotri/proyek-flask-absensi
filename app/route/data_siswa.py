
from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from app.model.data_siswa import data_siswa

siswa_bp = Blueprint('siswa', __name__)



@siswa_bp.route('/siswa')
def list_siswa():
    data = data_siswa.query.all()
    return render_template('siswa/index.html', data=data)

@siswa_bp.route('/siswa/create', methods=['GET', 'POST'])
def create_siswa():
    if request.method == 'POST':
        siswa = data_siswa(
            nisn=request.form.get('nisn'),
            nama=request.form.get('nama'),
            kelas=request.form.get('kelas'),
            email=request.form.get('email'),
            finger_id=request.form.get('finger_id'),
            alamat=request.form.get('alamat'),
            no_tlp=request.form.get('no_tlp'),
            prodi_id=request.form.get('prodi_id')
        )

        db.session.add(siswa)
        db.session.commit()

        return redirect(url_for('siswa.list_siswa'))

    return render_template('siswa/create.html')