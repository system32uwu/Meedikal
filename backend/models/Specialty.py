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

class _MpHasSpec(BaseModel):
    ciMp: int
    idSpec: int

    detail: Optional[str] = None

    specialtyTitle:str

    def __init__(self, ciMp:int,idSpec:int, detail:Optional[str]=None):
        self.ciMp = ciMp
        self.idSpec = idSpec
        self.detail = detail
        sp = Specialty.getById(self.idSpec)
        print(f"spppppp: {sp}")
        self.specialtyTitle = sp.title

@dataclass
class MpHasSpec(_MpHasSpec): 
    __tablename__ = 'mpHasSpec'
    
    ciMp: int
    idSpec: int

    detail: Optional[str] = None