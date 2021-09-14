from api.user import getTypes
from flask import request
from models.User import AuthUser

def requiresAuth(f):
    def decorator(*args,**kwargs):
        try:
            token = request.cookies['authToken']
        except:
            return {'error': 'Not authenticated (missing cookie)'}, 401

        ci = AuthUser.verifyToken(token)
        return f(ci, *args, **kwargs)
    return decorator

def requiresRole(role:str): # the required role to execute the action
    def decorator(f):
        def wrapper(ci:int, *args, **kwargs): # ci comes from the previous deco: requiresAuth
            userRoles = getTypes(ci)
            if role not in userRoles:
                return {'error': f'Insufficient permissions to perfom action. It should be done by: a {role} user'}, 401
            return f(*args, **kwargs)
        return wrapper

    return decorator