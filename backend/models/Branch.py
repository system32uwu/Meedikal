from ._base import BaseModel, TableWithId
from dataclasses import dataclass

@dataclass
class Branch(BaseModel, TableWithId):
    __tablename__ = 'branch'

    id:int
    name:str
    phoneNumber:str
    location:str
    googleMapsSrc:str

    def __init__(self, id:int=None, name:str=None, phoneNumber:str=None, location:str=None, googleMapsSrc:str=None):
       self.id = id
       self.name = name
       self.phoneNumber = phoneNumber
       self.location = location
       self.googleMapsSrc = googleMapsSrc

@dataclass
class ApTakesPlace(BaseModel): # Appointment < apTakesPlace > Branch
    __tablename__ = 'apTakesPlace'

    idAp: int
    idBranch: int