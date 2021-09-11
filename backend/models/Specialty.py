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
    
    ciMp: int
    idSpec: int

    detail: Optional[str] = None