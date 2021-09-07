from dataclasses import dataclass
from typing import Optional

@dataclass
class Specialty:
    __tablename__ = 'specialty'

    id: int
    title: str

@dataclass
class MpHasSpec: 
    __tablename__ = 'mpHasSpec'
    
    ciMp: int
    idSpec: int
    detail: Optional[str]