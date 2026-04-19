from extensions import db

class absensi_siswa(db.Model):
    __tablename__ = 'absensi_siswa'

    id = db.Column(db.Integer, primary_key=True)
    nisn = db.Column(db.Integer, nullable=True )
    waktu = db.Column(db.Integer, nullable=True )
    status = db.Column(db.String(20), nullable=False)
    tanggal = db.Column(db.Integer, nullable=True )


    siswa_id = db.Column(db.Integer, db.ForeignKey('data_siswa.id'), nullable= True)
    def __repr__(self):
        return f"<absensi_siswa {self.id}>"  