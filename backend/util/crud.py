from flask.json import jsonify

def crudReturn(result=None):
    if result is None:
        code = 404
    else:
        if isinstance(result,list):
            if len(result) < 1:
                code = 404
            else:
                code = 200

        elif isinstance(result, bool):
            if result == False:
                code = 404
            else:
                code = 200

        elif isinstance(result,int):
            if result < 1:
                code = 404
            else:
                code = 200
        else:
            code = 200
        
    return jsonify({"result": result}), code