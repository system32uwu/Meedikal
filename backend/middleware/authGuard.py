from util.errors import MissingCookieError, MissingRoleError
from flask import request
from api.user import getTypes
from models.User import AuthUser
from functools import wraps

def requiresAuth(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token = None
        try:
            token = request.cookies.get('authToken', None)
        except:
            pass

        if token is None:
            raise MissingCookieError
        else:
            ci = AuthUser.verifyToken(token)
            return f(*args, **kwargs, ci=ci)
        
    return decorator

def requiresRole(role:str): # the required role to execute the action
    def decorator(f):
        @requiresAuth
        @wraps(f)
        def wrapper(ci:int,*args, **kwargs): # ci comes from the previous deco: requiresAuth
            userRoles = getTypes(ci)
            if role not in userRoles:
                raise MissingRoleError(role)
            else:
                return f(*args, **kwargs)
        return wrapper

    return decorator