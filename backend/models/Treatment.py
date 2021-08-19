from dataclasses import dataclass
from . import db

@dataclass
class Treatment(db.Model):
    
    id: int
    name: str
    preview: str
    indications: object
    avgSessionTime: int # in seconds

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    preview = db.Column(db.String())
    indications = db.Column(db.JSON)
    avgSessionTime = db.Column(db.Integer)
    