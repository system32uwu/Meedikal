from dataclasses import asdict
from models._base import BaseModel
from .returnMessages import zeroRowReturn
from flask.json import jsonify
from flask import request

def crudReturn(result=None, paginationInfo=None):
    if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
        if isinstance(result,list):
            result = sum(result)
        
        if result < 1:
            return zeroRowReturn()
        else:
            return jsonify({"result": f"{result} rows were affected"}), 200
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
                        result[i] = asdict(result[i]) # make it json serializable
        
        elif isinstance(result, bool):
            if result == False:
                zeroRowReturn()
        
        elif isinstance(result,int):
            if result < 1:
                zeroRowReturn()

        data:dict = {"result": result}

        if paginationInfo:
            data['paginationInfo'] = paginationInfo

        return jsonify(data), 200