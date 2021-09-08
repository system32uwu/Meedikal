from models.db import BaseModel
from dataclasses import dataclass
from typing import Optional

@dataclass
class Specialty(BaseModel):
    __tablename__ = 'specialty'

    id: int
    title: str

@dataclass
class MpHasSpec(BaseModel): 
    __tablename__ = 'mpHasSpec'
    
    ciMp: int
    idSpec: int

    detail: Optional[str] = None