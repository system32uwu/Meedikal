from .User import User
from dataclasses import dataclass
from . import db

@dataclass
class Alert(db.Model): # allergies, behaviours, traumas...

    id: int
    title: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64), nullable=False) 

@dataclass
class UHasAlert(db.Model): # user < UHasAlert > Alert

    __tablename__ = 'uHasAlert'

    idAlert: int
    ciUser: int
    detail: str

    idAlert = db.Column(db.Integer, db.ForeignKey(Alert.id, ondelete='CASCADE'), primary_key=True)
    ciUser = db.Column(db.Integer, db.ForeignKey(User.ci, ondelete='CASCADE'))
    detail = db.Column(db.VARCHAR(256), nullable=False) 