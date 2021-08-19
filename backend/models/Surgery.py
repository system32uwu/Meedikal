from dataclasses import dataclass
from . import db

@dataclass
class Surgery(db.Model):
    
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 