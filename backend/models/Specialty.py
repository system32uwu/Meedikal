from dataclasses import dataclass
from . import db
from .User import MedicalPersonnel

@dataclass
class Specialty(db.Model):

    id: int
    title: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), unique=True, nullable=False) # It wouldn't make sense to store specialties with the same name multiple times, but neither would setting a 64 characters long PK do so.

@dataclass
class mpHasSpec(db.Model): 
    __tablename__ = 'mpHasSpec'
    
    ciMp: int
    idSpec: int
    detail: str

    ciMp = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.ci, ondelete='CASCADE'), primary_key=True)
    idSpec = db.Column(db.Integer, db.ForeignKey(Specialty.id, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(128))