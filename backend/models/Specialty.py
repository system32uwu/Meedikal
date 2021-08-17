from dataclasses import dataclass
from . import db
from .User import MedicalPersonnel

@dataclass
class Specialty(db.Model):

    ID: int
    title: str

    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), unique=True, nullable=False) # It wouldn't make sense to store specialties with the same name multiple times, but neither would setting a 64 characters long PK do so.

@dataclass
class mpHasSpec(db.Model): 
    
    CIMp: int
    IDSpec: int
    detail: str

    __tablename__ = 'mpHasSpec'
    CIMp = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.CI, ondelete='CASCADE'), primary_key=True)
    IDSpec = db.Column(db.Integer, db.ForeignKey(Specialty.ID, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(128))