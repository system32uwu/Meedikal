from ._base import BaseModel, TableWithId, db
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

    @classmethod
    def getBranchOfAp(cls, idAp):
        statement = f"""
        SELECT branch.* FROM branch, apTakesPlace
        WHERE apTakesPlace.idAp = ? AND apTakesPlace.idBranch = branch.id
        """

        result = db.execute(statement,[idAp]).fetchone()

        try:
            return cls(*result)
        except:
            return {}

@dataclass
class ApTakesPlace(BaseModel, TableWithId): # Appointment < apTakesPlace > Branch
    __tablename__ = 'apTakesPlace'

    idAp: int
    idBranch: int

    @classmethod
    def updateBranch(cls, idAp:int, data:dict):
        return cls.updateById(idAp,data, 'idAp')