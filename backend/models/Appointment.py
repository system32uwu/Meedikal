from .Treatment import Follows, Treatment
from .Exam import Exam, TakesEx
from .Form import From
from .User import MedicalAssitant, Patient, Doctor
from dataclasses import dataclass
from .db import db, BaseModel
from datetime import datetime, date, time
from sqlalchemy import Enum

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')
appointmentStatesEnum = Enum(*appointmentStates, name='appointmentState')

@dataclass
class Appointment(BaseModel):

    id: int
    name: str
    date: date
    state: Enum
    timeBegins: time
    timeEnds: time
    etpp: int # estimated time per patient, in seconds
    maxTurns: int # max patients to be attended

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(128), nullable=False) 
    date = db.Column(db.Date, nullable=False)
    state = db.Column(appointmentStatesEnum, nullable=False)
    timeBegins = db.Column(db.Time)
    timeEnds = db.Column(db.Time)
    etpp = db.Column(db.Integer, default=720) # 12 minutes default
    maxTurns = db.Column(db.Integer, default=1)

@dataclass
class AssignedTo(BaseModel): # Doctor < assignedTo > Appointment
    __tablename__ = 'assignedTo'

    idAp: int
    ciDoc: int

    idAp = db.Column(db.Integer, db.ForeignKey(Appointment.id, ondelete='CASCADE'), primary_key=True)
    ciDoc = db.Column(db.Integer, db.ForeignKey(Doctor.ci, ondelete='CASCADE'))

@dataclass
class AssistsAp(BaseModel): # MedicalAssistant < assistsAp > [ Doctor < assignedTo > Appointment ]
    __tablename__ = 'assistsAp'

    idAp: int
    ciMa: int
    time: datetime

    idAp = db.Column(db.Integer, db.ForeignKey(AssignedTo.idAp, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    ciMa = db.Column(db.Integer, db.ForeignKey(MedicalAssitant.ci, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    time = db.Column(db.Time, primary_key=True)

@dataclass
class AttendsTo(BaseModel): # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    idAp: int
    ciPa: int
    motive: str
    number: int
    time: time

    idAp = db.Column(db.Integer, db.ForeignKey(AssignedTo.idAp, ondelete='CASCADE'), primary_key=True)
    ciPa = db.Column(db.Integer, db.ForeignKey(Patient.ci, ondelete='CASCADE'), primary_key=True)
    motive = db.Column(db.VARCHAR(256))
    number = db.Column(db.Integer) # an appointment could either be managed with numbers, or time-based turns, or both. 
    time = db.Column(db.Time)

@dataclass
class Fills(BaseModel): # Patient < attendsTo > [ Doctor < assignedTo > Appointment ] < fills > [ Question < from > Form]
    
    idAp: int
    ciPa: int
    idForm: int
    idQuestion: int
    response: str

    idAp = db.Column(db.Integer, primary_key=True)
    ciPa = db.Column(db.Integer, primary_key=True)
    idQuestion = db.Column(db.Integer, primary_key=True)
    idForm = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.VARCHAR(256))

    __table_args__ = (db.ForeignKeyConstraint([idAp,ciPa], [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),
                      db.ForeignKeyConstraint([idQuestion,idForm], [From.idQ,From.idF], ondelete='CASCADE'))

@dataclass
class ApRefPrevAp(BaseModel): # self-relationship, used to make reference to a previous appointment
    __tablename__ = 'apRefPrevAp'

    idCurrAp: int
    ciPaCurrAp: int
    idPrevAp: int
    ciPaPrevAp: int

    idCurrAp = db.Column(db.Integer, primary_key=True)
    ciPaCurrAp = db.Column(db.Integer, primary_key=True)
    idPrevAp = db.Column(db.Integer, primary_key=True)
    ciPaPrevAp = db.Column(db.Integer, primary_key=True)

    __table_args__ = (
                      db.ForeignKeyConstraint(
                      [idCurrAp,ciPaCurrAp],
                      [AttendsTo.idAp,AttendsTo.ciPa],
                       ondelete='CASCADE',
                       name='fk_currAp'),
                       db.ForeignKeyConstraint(
                      [idPrevAp,ciPaPrevAp],
                      [AttendsTo.idAp,AttendsTo.ciPa],
                       ondelete='CASCADE',
                       name='fk_prevAp'),
                       )

@dataclass
class ApRefExam(BaseModel): # [ attendsTo ] < apRefExam > [ takesEx ]
    __tablename__ = 'apRefExam'

    idAp: int
    ciPaAp: int

    idExTaken: int
    idEx: int
    ciPaEx: int

    idAp = db.Column(db.Integer, primary_key=True)
    ciPaAp = db.Column(db.Integer, primary_key=True)
    
    idExTaken = db.Column(db.Integer, primary_key=True)
    idEx = db.Column(db.Integer, primary_key=True)
    ciPaEx = db.Column(db.Integer, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint(
                        [idAp,ciPaAp],
                        [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),
                      db.ForeignKeyConstraint(
                        [idExTaken,idEx,ciPaEx],
                      [TakesEx.idExTaken, TakesEx.idEx, TakesEx.ciPa], ondelete='CASCADE'),)

@dataclass
class ApRefTr(BaseModel): # [ attendsTo ] < apRefTr > [ follows ]
    __tablename__ = 'apRefTr'

    idAp: int
    ciPaAp: int

    idFollows: int
    idTreatment: int
    ciPaTr: int

    idAp = db.Column(db.Integer, primary_key=True)
    ciPaAp = db.Column(db.Integer, primary_key=True)
    
    idFollows = db.Column(db.Integer, primary_key=True)
    idTreatment = db.Column(db.Integer, primary_key=True)
    ciPaTr = db.Column(db.Integer, primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint(
                        [idAp,ciPaAp],
                        [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),
                      db.ForeignKeyConstraint(
                        [idFollows,idTreatment,ciPaTr],
                      [Follows.idFollows, Follows.idTreatment, Follows.ciPa], ondelete='CASCADE'),)

@dataclass
class SuggestsTr(BaseModel): # [ attendsTo ] < suggestsTr > Treatment
    __tablename__ = 'suggestsTr'

    idAp: int
    ciPaAp: int
    idTreatment: int

    idAp = db.Column(db.Integer, primary_key=True)
    ciPaAp = db.Column(db.Integer, primary_key=True)
    idTreatment = db.Column(db.Integer, db.ForeignKey(Treatment.id, ondelete='CASCADE'), primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint(
                        [idAp,ciPaAp],
                        [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),)

@dataclass
class RequiresEx(BaseModel): # [ attendsTo ] < requiresEx > Exam
    __tablename__ = 'requiresEx'

    idAp: int
    ciPaAp: int
    idEx: int

    idAp = db.Column(db.Integer, primary_key=True)
    ciPaAp = db.Column(db.Integer, primary_key=True)
    idEx = db.Column(db.Integer, db.ForeignKey(Exam.id, ondelete='CASCADE') ,primary_key=True)

    __table_args__ = (db.ForeignKeyConstraint(
                        [idAp,ciPaAp],
                        [AttendsTo.idAp,AttendsTo.ciPa], ondelete='CASCADE'),)