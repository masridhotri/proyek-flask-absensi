from extensions import db

class DataProgli(db.Model):
    __tablename__ = 'data_progli'

    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(50), nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    students = db.relationship('data_siswa', backref='prodi', lazy=True)   

    def __repr__(self):
        return f"<DataProgli {self.nama}>"