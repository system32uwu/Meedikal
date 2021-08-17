from dataclasses import dataclass
from . import db

@dataclass
class Branch(db.Model):

    ID: int
    name: str
    phoneNumber: str
    location: str

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), unique=True, nullable=False) 
    phoneNumber = db.Column(db.VARCHAR(64), nullable=False) 
    location = db.Column(db.VARCHAR(64), nullable=False) 
