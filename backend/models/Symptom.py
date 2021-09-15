from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from typing import Optional

@dataclass
class Symptom(BaseModel, TableWithId):
    __tablename__ = 'symptom'

    id: int
    name: str
    description: Optional[str] = None

    def __init__(self, id:int=None, name:str=None, description:str=None):
        self.id = id
        self.name = name
        self.description = description

@dataclass
class RegistersSy(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersSy > Symptom
    __tablename__ = 'registersSy'

    idAp: int
    ciPa: int
    idSy: int
    detail: Optional[str] = None