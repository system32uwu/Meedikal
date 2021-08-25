from .Appointment import AttendsTo
from dataclasses import dataclass
from .db import db, BaseModel

@dataclass
class ClinicalSign(BaseModel):
    __tablename__ = 'clinicalSign'

    id: int
    name: str
    description: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 
    description = db.Column(db.VARCHAR(512)) 

@dataclass
class registersCs(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersCs > ClinicalSign
    __tablename__ = 'registersCs'

    idAp: int
    ciPa: int
    idCs: int
    detail: str

    idAp = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    idCs = db.Column(db.Integer, db.ForeignKey(ClinicalSign.id, ondelete='CASCADE'), primary_key=True)
    detail = db.Column(db.VARCHAR(256))

    __table_args__ = (db.ForeignKeyConstraint([idAp,ciPa], [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),)
