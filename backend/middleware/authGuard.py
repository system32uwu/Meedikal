from util.errors import MissingCookieError, MissingRoleError
from flask import session
from models.User import User, AuthUser
from functools import wraps

def requiresAuth(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token = None
        try:
            token = session.get('authToken', None)
        except: # flask out of context error (raises when starting the app)
            pass

        if token is None:
            raise MissingCookieError()
        else:
            ci = AuthUser.verifyToken(token)
            return f(*args, **kwargs, ci=ci)
        
    return decorator

def requiresRole(roles:list[str]): # the required roles to execute the action
    def decorator(f):
        @requiresAuth
        @wraps(f)
        def wrapper(ci:int,*args, **kwargs): # ci comes from the previous deco: requiresAuth
            userRoles = User.getRoles(ci)
            for r in roles:
                if r in userRoles:
                    return f(*args, **kwargs)
            raise MissingRoleError(roles)

        return wrapper

    return decorator

def getCurrentRole(f):
    @requiresAuth
    @wraps(f)
    def wrapper(ci:int,*args, **kwargs): # ci comes from the previous deco: requiresAuth
        currentRole = session.get('currentRole', None)
            
        if not currentRole:
            currentRole = User.getRoles(ci)[0]
            session['currentRole'] = currentRole
                
        return f(*args, **kwargs, currentRole=currentRole, ci=ci)
    return wrapper