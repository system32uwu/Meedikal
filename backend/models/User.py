from dataclasses import asdict, dataclass
from werkzeug.security import check_password_hash
from .db import BaseModel, db
from datetime import datetime
from typing import Optional

class SharedUserMethods(BaseModel):

    @classmethod
    def getByCi(cls, ci: int):
        return cls.filter({'ci': ci}, returns='one')

@dataclass
class User(SharedUserMethods):
    __tablename__ = 'user'
    
    ci: int
    name1: str
    surname1: str
    sex: str
    birthdate: datetime
    location: str
    email: str
    password: str
    name2: Optional[str] = None
    surname2: Optional[str] = None
    genre: Optional[str] = None
    active: Optional[bool] = True

    @classmethod
    def update(cls, conditions: dict= {}, logicalOperator: str = 'AND'):
        try:
            conditionList = [f"{key} {value.get('operator', '=')} ?"
                            for key, value in conditions.items()]
        except:
            conditionList = [f"{key} = ?"
                            for key in conditions.keys()]
        
        # can't compare hashes (even if it's the same password) since they will always be different.
        oldConditionList = conditionList.copy()
        oldConditionList.remove("password = ?")

        values = [v.get('value', v)
                 for k, v in conditions.items() 
                 if k != 'password'] 

        newValues = [v.get('newValue', v.get('value', v)) 
                    for v in conditions.values()]
        
        values = newValues + values

        statement = f"""
        UPDATE {cls.__tablename__}
        {'SET ' + ', '.join(conditionList) if len(conditionList) > 0 else ''}
        {'WHERE ' + f' {logicalOperator} '.join(oldConditionList) if len(oldConditionList) > 0 else ''}
        """

        cursor = db.cursor()
        cursor.execute(statement,values)
        db.commit()
        cursor.close()

        for key, value in conditions.items():
            conditions[key] = value.get("newValue", value.get("value"))

        return cls.filter(conditions) # return the affected rows

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

@dataclass # since phone is a multivalued attribute, it has its own table.
class UserPhone(BaseModel):
    __tablename__ = 'userPhone'

    ci: int
    phone: str # since phone numbers aren't real numbers it's better to store them as strings. Some countries (like Uruguay), start their cellphone numbers with a 0, which on input would be ignored by the DBMS if the datatype was Integer. 

    @classmethod
    def getByCi(cls, ci: int):
        return cls.filter({'ci': ci}, returns='all')

class CategorizedUser(SharedUserMethods):
    ci: int
    user: User = None

    def __init__(self):
        self.user = User(**db.execute("SELECT * FROM user WHERE ci=?", [self.ci]).fetchone())
        return self.user

@dataclass
class Patient(CategorizedUser):
    __tablename__ = 'patient'
    
@dataclass # users from the medical personnel, those without further categorization (either doctor or medical assitant), will be stored only in this table and have limited permissions and access
class MedicalPersonnel(CategorizedUser):
    __tablename__ = 'medicalPersonnel'

@dataclass # users from the medical personnel, who are doctors. 
class Doctor(CategorizedUser):
    __tablename__ = 'doctor'

@dataclass # users from the medical personnel, who are medical assistants (i.e: nurses)
class MedicalAssitant(CategorizedUser):
    __tablename__ = 'medicalAssistant'

@dataclass
class Administrative(CategorizedUser):
    __tablename__ = 'administrative'