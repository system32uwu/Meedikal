from models.db import BaseModel
from dataclasses import dataclass
from typing import Optional

@dataclass
class Specialty(BaseModel):
    __tablename__ = 'specialty'

    id: int
    title: str

    def __init__(self,id:int=None,title:str=None):
        self.id = id
        self.title = title

    @classmethod 
    def getById(cls, id:int):
        return cls.filter({'id': id}, returns='one')

@dataclass
class MpHasSpec(BaseModel): 
    __tablename__ = 'mpHasSpec'

    idSpec: int
    ciMp: int

    detail: Optional[str] = None
    title: str = None

    def __init__(self,idSpec,ciMp,detail:str=None):
        self.idSpec = idSpec
        self.ciMp = ciMp
        self.detail = detail
        self.title = Specialty.getById(idSpec).title # field that makes sense adding when returning to client, for the user knowing the id is meaningless.