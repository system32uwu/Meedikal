from .User import User
from dataclasses import dataclass
from . import db
from datetime import datetime

@dataclass
class Notification(db.Model):

    ID: int
    date: datetime
    title: str
    content: str

    ID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.VARCHAR(64), nullable=False) 
    content = db.Column(db.VARCHAR(512)) 

@dataclass
class UReceivesNot(db.Model): # user < UReceivesNot > notification

    __tablename__ = 'uReceivesNot'

    IDNot: int
    CIUser: int

    IDNot = db.Column(db.Integer, db.ForeignKey(Notification.ID, ondelete='CASCADE'), primary_key=True)
    CIUser = db.Column(db.Integer, db.ForeignKey(User.CI, ondelete='CASCADE'))
    