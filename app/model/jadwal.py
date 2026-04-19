from extensions import db

class jadwal(db.Model):
    __tablename__ = 'jadwal'

    id = db.Column(db.Integer, primary_key=True)
    hari = db.Column(db.String(100), nullable=False)
    jam_masuk = db.Column(db.String(100), nullable=False)
    jam_keluar = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"<jadwal {self.id}>"