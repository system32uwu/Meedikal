from flask.json import jsonify

def crudReturn(result=None): # kwarg
    if result is None:
        code = 404
    else:
        if isinstance(result,list):
            if len(result) == 0:
                code = 404

        elif isinstance(result, bool):
            if result == False:
                code = 404

        code = 200
        
    return jsonify({"result": result}), code