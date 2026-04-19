from extensions import db

class data_siswa(db.Model):
    __tablename__ = 'data_siswa'

    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.Integer, nullable=True )
    nama = db.Column(db.String(50), nullable=True )
    kelas = db.Column(db.Integer, nullable=True )
    email = db.Column(db.String(50), nullable=True )
    email_verified = db.Column(db.String(100), unique=True, nullable=False)
    finger_id = db.Column(db.Integer, unique=True, nullable=False)
    alamat = db.Column(db.String(50), nullable=False)
    no_tlp = db.Column(db.Integer, nullable=True)

    prodi_id = db.Column(db.Integer, db.ForeignKey('data_progli.id'), nullable= True)
    def __repr__(self):
        return f"<data_siswa {self.id}>"