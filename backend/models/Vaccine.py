from dataclasses import dataclass
from . import db

@dataclass
class Vaccine(db.Model):
    ID: int
    name: str
    validity: int # in days

    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    validity = db.Column(db.Integer)
