from ._base import BaseModel, TableWithId
from dataclasses import dataclass
from typing import Optional

@dataclass
class Disease(BaseModel, TableWithId):
    __tablename__ = 'disease'

    id:int
    name:str
    description:Optional[str]

    def __init__(self, id:int=None, name:str=None, description:str=None):
        self.id = id
        self.name = name
        self.description = description

@dataclass
class Diagnoses(BaseModel): # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < diagnoses > Disease
    __tablename__ = 'diagnoses'

    idAp: int
    ciPa: int
    idDis: int
    detail: Optional[str] = None