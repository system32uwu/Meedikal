from api.user import getTypes
from flask import request
from models.User import AuthUser
from functools import wraps
def requiresAuth(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        try:
            token = request.cookies['authToken']
        except:
            return {'error': 'Not authenticated (missing cookie)'}, 401
            
        AuthUser.verifyToken(token)
        return f(*args, **kwargs)
    return decorator

def requiresRole(role:str): # the required role to execute the action
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs): # ci comes from the previous deco: requiresAuth
            ci = AuthUser.verifyToken(request.cookies['authToken'])
            userRoles = getTypes(ci)
            if role not in userRoles:
                return {'error': f'Insufficient permissions to perfom action. It should be done by: a {role} user'}, 401
            return f(*args, **kwargs)
        return wrapper

    return decorator