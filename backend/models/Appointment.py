from datetime import datetime, timedelta
from ._base import BaseModel, TableWithId, db
from .User import Patient
from dataclasses import dataclass
from dateutil.parser import isoparse

from typing import Optional

appointmentStates = ('OK','CANCELLED', 'RESCHEDULING')
DATE_TIME_STRING_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

@dataclass
class Appointment(BaseModel, TableWithId):
    __tablename__ = 'appointment'

    id:int
    name:str
    state:str
    date:str

    startsAt:Optional[str] = None
    endsAt:Optional[str] = None
    etpp:Optional[int] = None # estimated time per patient, in minutes
    maxTurns:Optional[int] = None # max patients to be attended

    def __init__(self, id:int=None, name:str=None,state:str=None,date:str=None,
                startsAt:str=None, endsAt:str=None, etpp:int=None, maxTurns:int=None):
        self.id = id
        self.name = name
        self.state = state
        
        try:
            isoparse(date)
            self.date = date
        except:
            self.date = None
        
        try:
            isoparse(startsAt)
            self.startsAt = startsAt
        except:
            self.startsAt = None

        try:
            isoparse(endsAt)
            self.endsAt = endsAt
        except:
            self.endsAt = None
            
        self.etpp = etpp
        self.maxTurns = maxTurns

    @classmethod 
    def generateTimes(cls, startsAt:datetime, endsAt:datetime, etpp:int, idAp:int):
        datetimes = [(idAp, startsAt.strftime(DATE_TIME_STRING_FORMAT))]

        _startsAt = startsAt

        while _startsAt + timedelta(minutes=etpp) < endsAt:
            _startsAt += timedelta(minutes=etpp)
            datetimes.append((idAp, _startsAt.strftime(DATE_TIME_STRING_FORMAT)))

        statement = f"""
        INSERT INTO freeTimes (idAp, value) VALUES (?, ?)
        """            

        try:
            db.cursor().executemany(statement, datetimes)

            db.commit()

            return True
        except:
            return False    

    @classmethod
    def generateTurns(cls, maxTurns:int, idAp:int) -> bool:
        _turns = list(range(1, maxTurns + 1))
        turns = []
        for turn in _turns:
            turns.append((idAp, turn))

        statement = f"""
        INSERT INTO freeTurns (idAp, value) VALUES (?, ?)
        """
        try:
            db.cursor().executemany(statement, turns)

            db.commit()

            return True
        except Exception:
            return False

    @classmethod
    def save(cls, conditions: dict= {}, returns='one'):
        try:
            if conditions.get('startsAt', None) is not None and conditions.get('endsAt', None) is not None:
                startsAt = datetime.strptime(conditions['startsAt'], DATE_TIME_STRING_FORMAT)
                endsAt = datetime.strptime(conditions['endsAt'], DATE_TIME_STRING_FORMAT)

                diff = endsAt - startsAt
                diffMins = diff.total_seconds() / 60
                
                if diffMins < 10:
                    raise 'time interval too short.'

                etpp = conditions.get('etpp', None)

                maxTurns = conditions.get('maxTurns', None)
                
                if etpp is None and maxTurns is None:
                    etpp = 10
                    maxTurns = int(diffMins // etpp) # floor
                elif etpp is None:
                    etpp = int(diffMins // maxTurns) # floor
                elif maxTurns is None:
                    maxTurns = int(diffMins // etpp) # floor
                
                if diffMins // maxTurns < 1.0:
                    raise 'number of turns too high for the chosen time interval.'
                elif diffMins // etpp < 1.0:
                    raise 'etpp too high for the chosen time interval.'

                conditions['maxTurns'] = maxTurns
                conditions['etpp'] = etpp

                result = super().save(conditions, returns)

                cls.generateTurns(maxTurns, result.id)
                cls.generateTimes(startsAt, endsAt, etpp, result.id)

                return result
            else: 
                raise 'no times provided'
        except Exception as exc:
                _exc = str(exc)

                if 'short' in _exc:
                    conditions['startsAt'] = None
                    conditions['endsAt'] = None
                elif 'turns' in _exc:
                    conditions['maxTurns'] = None
                elif 'etpp' in _exc:
                    conditions['etpp'] = None
                else: # invalid datetimes
                    conditions['startsAt'] = None
                    conditions['endsAt'] = None

                result = super().save(conditions, returns)

                if maxTurns is not None:
                    cls.generateTurns(maxTurns, result.id)

                return result

@dataclass
class AssignedTo(BaseModel): # Doctor < assignedTo > Appointment
    __tablename__ = 'assignedTo'

    idAp: int
    ciDoc: int
    
@dataclass
class AttendsTo(BaseModel): # Patient < attendsTo > [ Doctor < assignedTo > Appointment]
    __tablename__ = 'attendsTo'

    idAp: int
    ciPa: int

    motive: Optional[str] = None
    time: Optional[str] = None
    number: Optional[int] = None
    notes: Optional[str] = None

    def __init__(self,idAp:int,ciPa:int,motive:str=None,time:str=None, number:int=None, notes:str=None):
        self.idAp = idAp
        self.ciPa = ciPa
        self.motive = motive
        self.notes = notes
              
        try:
            isoparse(time)
            self.time = time
        except:
            self.time = None
            
        self.number = number

    @classmethod
    def getPatients(cls, idAp) -> list[Patient]:
        statement = f"""
        SELECT ciPa from attendsTo
        WHERE idAp = ?
        """

        result = db.execute(statement, [idAp]).fetchall()

        if result:
            return [Patient(*p) for p in result]
        else:
            return []
