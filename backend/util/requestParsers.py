from models.User import *
from flask import Request

def wrapWithCi(tablename:str) -> str:
    return f'{tablename}.ci'

def parseUserType(request:Request) -> str:
    try:
        data:dict = request.get_json()
        return data['extraFilters']['userType']
        # for k in data.keys():
        #     if wrapWithCi(Patient.__tablename__) == k:
        #         return Patient.__tablename__
        #     elif wrapWithCi(Administrative.__tablename__) == k:
        #         return Administrative.__tablename__
        #     elif wrapWithCi(MedicalPersonnel.__tablename__) == k:
        #         return MedicalPersonnel.__tablename__
        #     elif wrapWithCi(Doctor.__tablename__) == k:
        #         return Doctor.__tablename__
        #     elif wrapWithCi(MedicalAssitant.__tablename__) == k:
        #         return MedicalAssitant.__tablename__
    except:
        return None