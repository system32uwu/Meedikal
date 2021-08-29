from datetime import datetime
from .User import Doctor, MedicalAssitant, Patient
from dataclasses import dataclass
from .db import db, BaseModel

@dataclass
class Surgery(BaseModel):
    
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), unique=True, nullable=False) 

@dataclass 
class TakesSurg(BaseModel):
    __tablename__ = 'takesSurg'

    idTakenSurg: int
    idSurg: int
    ciPa: int
    date: datetime
    startedAt: datetime
    finishedAt: datetime
    result: str

    idTakenSurg = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idSurg = db.Column(db.Integer, db.ForeignKey(Surgery.id, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime)
    startedAt = db.Column(db.DateTime)
    finishedAt = db.Column(db.DateTime)
    result = db.Column(db.VARCHAR(128))

@dataclass 
class HandlesSurg(BaseModel):
    __tablename__ = 'handlesSurg'

    idTakenSurg: int
    idSurg: int
    ciPa: int
    ciDoc: int

    idTakenSurg = db.Column(db.Integer, primary_key=True)
    idSurg = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    ciDoc = db.Column(db.Integer, db.ForeignKey(Doctor.ci, ondelete='CASCADE'), primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([idTakenSurg,idSurg,ciPa],
                    [TakesSurg.idTakenSurg,TakesSurg.idSurg,TakesSurg.ciPa], ondelete='CASCADE'),)

@dataclass 
class AssistsSurg(BaseModel):
    __tablename__ = 'assistsSurg'

    idTakenSurg: int
    idSurg: int
    ciPa: int
    ciMa: int

    idTakenSurg = db.Column(db.Integer, primary_key=True)
    idSurg = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    ciMa = db.Column(db.Integer, db.ForeignKey(MedicalAssitant.ci, ondelete='CASCADE'), primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint([idTakenSurg,idSurg,ciPa],
                    [TakesSurg.idTakenSurg,TakesSurg.idSurg,TakesSurg.ciPa], ondelete='CASCADE'),)