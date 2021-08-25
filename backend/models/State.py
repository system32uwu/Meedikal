from dataclasses import dataclass
from .db import db, BaseModel
from .User import Patient
from datetime import datetime

@dataclass
class State(BaseModel):

    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(64), nullable=False)

@dataclass
class registersSt(BaseModel): # Patient < registersSt > State 

    __tablename__ = 'registersSt'

    ciPa: int
    idState: int
    fromDate: datetime
    toDate: datetime
    notes: str

    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    idState = db.Column(db.Integer, db.ForeignKey(State.id, ondelete='CASCADE'), primary_key=True)
    fromDate = db.Column(db.DateTime, primary_key=True)
    toDate = db.Column(db.DateTime)
    notes = db.Column(db.VARCHAR(256))