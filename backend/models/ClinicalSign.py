from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from typing import Optional

@dataclass
class ClinicalSign(BaseModel, TableWithId):
    __tablename__ = 'clinicalSign'

    id: int
    name: str
    description: Optional[str] = None
    
    def __init__(self, id:int=None, name:str=None, description:str=None):
        self.id = id
        self.name = name
        self.description = description

@dataclass
class RegistersCs(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersCs > ClinicalSign
    __tablename__ = 'registersCs'

    idAp: int
    ciPa: int
    idCs: int
    detail: Optional[str] = None