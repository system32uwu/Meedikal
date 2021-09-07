from dataclasses import dataclass

@dataclass
class ClinicalSign:
    __tablename__ = 'clinicalSign'

    id: int
    name: str
    description: str

@dataclass
class RegistersCs: # { Patient < attendsTo > [ Doctor < assignedTo > Appointment] } < registersCs > ClinicalSign
    __tablename__ = 'registersCs'

    idAp: int
    ciPa: int
    idCs: int
    detail: str