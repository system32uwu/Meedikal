from flask import request
from functools import wraps

def passJsonData(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        data = request.get_json()
        return f(*args, **kwargs, data=data)
        
    return decorator