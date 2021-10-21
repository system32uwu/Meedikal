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
    def updateById(cls, id:int, data:dict):
        sets = [f'{k} = ?' for k in data.keys()]

        statement = f"""
        UPDATE {cls.__tablename__} SET
        {', '.join(sets)}
        WHERE id = ?
        """

        values = [v for v in data.values()] + [id]
        cursor = db.cursor()
        cursor.execute(statement, values)
        db.commit()

        return cursor.rowcount

@dataclass
class ApTakesPlace(BaseModel): # Appointment < apTakesPlace > Branch
    __tablename__ = 'apTakesPlace'

    idAp: int
    idBranch: int