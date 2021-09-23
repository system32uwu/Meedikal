from models.User import *
from flask import Request

def parseUserType(request:Request) -> str:
    try:
        return request.get_json()['extraFilters']['userType']
    except:
        return None