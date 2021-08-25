from .User import User
from dataclasses import dataclass
from .db import db, BaseModel
from datetime import datetime

@dataclass
class Notification(BaseModel):

    id: int
    date: datetime
    title: str
    content: str

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.VARCHAR(64), nullable=False) 
    content = db.Column(db.VARCHAR(512)) 

@dataclass
class UReceivesNot(BaseModel): # user < UReceivesNot > notification

    __tablename__ = 'uReceivesNot'

    idNot: int
    ciUser: int

    idNot = db.Column(db.Integer, db.ForeignKey(Notification.id, ondelete='CASCADE'), primary_key=True)
    ciUser = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'))
    