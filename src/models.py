from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(25), unique=False, nullable=False)
    email = db.Column(db.String(25), unique=False, nullable=True)
    address = db.Column(db.String(50), unique=False, nullable=True)
    phone = db.Column(db.String(12), unique=False, nullable=True)

    def __repr__(self):
        return '<Contact %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone
            # do not serialize the password, its a security breach
        }