from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from typing import Optional

@dataclass
class ClinicalSign(BaseModel, TableWithId):
    __tablename__ = 'clinicalSign'

    id: int
    name: str
    description: Optional[str]

@dataclass
class RegistersCs(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersCs > ClinicalSign
    __tablename__ = 'registersCs'

    idAp: int
    ciPa: int
    idCs: int
    detail: Optional[str]