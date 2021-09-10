from models.db import BaseModel
from dataclasses import dataclass
from typing import Optional

@dataclass
class Specialty(BaseModel):
    __tablename__ = 'specialty'

    id: int
    title: str

    @classmethod 
    def getById(cls, id:int):
        return cls.filter({'id': id}, returns='one')

@dataclass
class MpHasSpec(BaseModel): 
    __tablename__ = 'mpHasSpec'
    
    ciMp: int
    idSpec: int

    detail: Optional[str] = None
    spTitle: str = None

    def __init__(self,ciMp:int,idSpec:int, detail:Optional[str]=None):
        self.ciMp = ciMp
        self.idSpec = idSpec
        self.detail = detail
        self.spTitle = Specialty.getById(self.idSpec).title