from util.errors import MissingCookieError, MissingRoleError
from flask import session, request
from models.User import User,AuthUser
from functools import wraps

def requiresAuth(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token = None
        try:
            token = session['authToken']
        except: # flask out of context error (raises when starting the app)
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
            userRoles = User.getRoles(ci)
            if role not in userRoles:
                raise MissingRoleError(role)
            else:
                return f(*args, **kwargs)
        return wrapper

    return decorator