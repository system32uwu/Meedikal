from dataclasses import asdict
from models._base import BaseModel
from .returnMessages import zeroRowReturn
from flask.json import jsonify
from flask import request

def crudReturn(result=None):
    if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
        if result < 1:
            return zeroRowReturn()
        else:
            return jsonify({"result": f"{result} rows were affected"}, 200)
    else:
        if result is None:
            zeroRowReturn()

        elif isinstance(result, BaseModel):
            result = asdict(result)

        elif isinstance(result,list):
            if len(result) < 1:
                zeroRowReturn()
            else:
                for i in range(len(result)):
                    if not isinstance(result[i],dict):
                        result[i] = asdict(result[i])
        
        elif isinstance(result, bool):
            if result == False:
                zeroRowReturn()
        
        elif isinstance(result,int):
            if result < 1:
                zeroRowReturn()

        return jsonify({"result": result}), 200