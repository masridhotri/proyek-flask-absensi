from extensions import db

class device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    No_seri = db.Column(db.Integer, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    nama = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"<device {self.id}>"