from extensions import db

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return f"<user {self.id}>"