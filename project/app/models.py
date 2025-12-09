from app import db
from datetime import datetime


# Attributs User: id, email (unique), last_name, first_name, birth_date.  
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date.isoformat(),
        }

    def __repr__(self):
        return f"User (email = {self.email}, last_name = {self.last_name}, first_name = {self.first_name}, birth_date = {self.birth_date})"

