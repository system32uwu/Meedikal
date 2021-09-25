from util.returnMessages import genericErrorReturn
from flask import request
from functools import wraps

def passJsonData(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        data = request.get_json()
        return f(*args, **kwargs, data=data)
        
    return decorator

def passFile(allowedExtensions:list[str]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            file = request.files.get('file', None)
            extension = file.filename.rsplit('.')[1].lower()
            if extension not in allowedExtensions:
                return genericErrorReturn(f'extension {extension} not allowed.', f'allowed extensions: {", ".join(allowedExtensions)}')

            return f(*args, **kwargs, file=file)
        
        return wrapper

    return decorator