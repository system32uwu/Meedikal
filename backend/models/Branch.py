from dataclasses import dataclass

@dataclass
class Branch:
    __tablename__ = 'branch'

    id: int
    name: str
    phoneNumber: str
    location: str

@dataclass
class ApTakesPlace: # Appointment < apTakesPlace > Branch
    __tablename__ = 'apTakesPlace'

    idAp: int
    idBranch: int