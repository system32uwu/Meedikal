from util.errors import ExtensionNotAllowedError
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
                raise ExtensionNotAllowedError(allowedExtensions, extension)
            else:
                return f(*args, **kwargs, file=file)
        
        return wrapper

    return decorator

def paginated(offset:int=0, limit:int=10, max:int=10):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _offset = offset
            _limit = limit

            data = request.args

            if 'offset' in data:
                _offset = int(data['offset'])

            if 'limit' in data:
                _limit = int(data['limit'])

            if _offset < 0:
                _offset = 0

            if _limit > max:
                _limit = max

            if _offset > _limit:
                _offset = _limit - 1

            return f(*args, **kwargs, offset=_offset, limit=_limit)
        
        return wrapper
    return decorator