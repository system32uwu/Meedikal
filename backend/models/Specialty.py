from models.db import BaseModel, TableWithId
from dataclasses import dataclass
from typing import Optional

@dataclass
class Specialty(BaseModel, TableWithId):
    __tablename__ = 'specialty'

    id:int
    title:str

    def __init__(self,id:int=None,title:str=None):
        self.id = id
        self.title = title

@dataclass
class MpHasSpec(BaseModel): 
    __tablename__ = 'mpHasSpec'

    idSpec:int
    ciMp:int

    detail:Optional[str] = None

    def __init__(self,idSpec,ciMp,detail:str=None):
        self.idSpec = idSpec
        self.ciMp = ciMp
        self.detail = detail