from .User import MedicalPersonnel
from dataclasses import dataclass
from . import db
from datetime import datetime

@dataclass
class Form(db.Model):

    id: int
    title: str
    preview: str # path of a screenshot of the form
    content: object # serialized components (labels, input fields, checkboxes...)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(64)) 
    preview = db.Column(db.String())
    content = db.Column(db.JSON)

@dataclass
class Question(db.Model):

    id: int
    text: str

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.VARCHAR(64), nullable=False) 

@dataclass # question < from > form
class From(db.Model):

    idQ: int # id of the question
    idF: str # id of the form

    idQ = db.Column(db.Integer, db.ForeignKey(Question.id, ondelete='CASCADE'), primary_key=True)
    idF = db.Column(db.Integer, db.ForeignKey(Form.id, ondelete='CASCADE'), primary_key=True)

@dataclass # medicalPersonnel user < designed > form
class Designed(db.Model):

    ciMp: int # id of the user
    idF: str # id of the form
    date: datetime # date and time the form is created / updated
    isMainAuthor: bool # if the user is the creator of the form
    changelog: str # log what was added or removed, like version control with git.

    ciMp = db.Column(db.Integer, db.ForeignKey(MedicalPersonnel.ci, ondelete='CASCADE'), primary_key=True)
    idF = db.Column(db.Integer, db.ForeignKey(Form.id, ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True, nullable=False)
    isMainAuthor = db.Column(db.BOOLEAN, default=True, nullable=False)
    changelog = db.Column(db.String())
