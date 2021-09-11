from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from typing import Optional

@dataclass
class Symptom(BaseModel, TableWithId):
    __tablename__ = 'symptom'

    id: int
    name: str
    description: Optional[str] = None

@dataclass
class RegistersSy(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersSy > Symptom
    __tablename__ = 'registersSy'

    idAp: int
    ciPa: int
    idSy: int
    detail: Optional[str] = None