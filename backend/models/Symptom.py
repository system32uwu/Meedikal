from dataclasses import dataclass
from typing import Optional

@dataclass
class Symptom:
    __tablename__ = 'symptom'

    id: int
    name: str
    description: Optional[str] = None

@dataclass
class RegistersSy: # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersSy > Symptom
    __tablename__ = 'registersSy'

    idAp: int
    ciPa: int
    idSy: int
    detail: Optional[str] = None