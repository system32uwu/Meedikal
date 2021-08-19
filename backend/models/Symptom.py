from .Appointment import AttendsTo
from dataclasses import dataclass
from . import db

@dataclass
class Symptom(db.Model):
    
    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class registerSy(db.Model): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersSy > Symptom
    __tablename__ = 'registersSy'

    idAp: int
    ciPa: int
    idSy: int
    detail: str

    idAp = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    idSy = db.Column(db.Integer, db.ForeignKey(Symptom.id, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(256))

    __table_args__ = (db.ForeignKeyConstraint([idAp,ciPa], [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),)
