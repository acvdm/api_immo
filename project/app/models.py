from app.common.database import db
from sqlalchemy import func
from sqlalchemy.orm import relationship



class User(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    properties = relationship("Property", back_populates="owner", lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }



class Property(db.Model):
    __tablename__ = 'properties'


    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    size = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())

    owner = relationship("User", back_populates="properties")
    rooms = relationship("Room", back_populates="parent_property", lazy=True, cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'city': self.city,
            'price': self.price,
            'size': self.size,
            'created_at': self.created_at.isoformat()
        }
    

 
class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())

    parent_property = relationship("Property", back_populates="rooms")


    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'type': self.type,
            'size': self.size,
            'created_at': self.created_at.isoformat()
        }