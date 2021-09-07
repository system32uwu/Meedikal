from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Disease:
    __tablename__ = 'disease'

    id: int
    name: str
    description: Optional[str]

@dataclass
class Diagnoses: # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < diagnoses > Disease
    __tablename__ = 'diagnoses'

    idAp: int
    ciPa: int
    idDis: int
    detail: Optional[str]