def recorddoesntExist(tablename:str):
    return {"error": f"{tablename} doesn't exist"}, 400

def recordAlreadyExists(tablename:str):
    return {"error": f"{tablename} already exists"}, 400

def notFound(tablename:str):
    return {"error": f"no {tablename} was found"}, 400

def provideData():
    return {"error": "no data was provided"}, 400

def recordCUDSuccessfully(tablename:str,method:str):
    if method == 'POST':
        return {"result": f"{tablename} created successfully"}, 200
    elif method == 'PUT' or method == 'PATCH':
        return {"result": f"{tablename} updated successfully"}, 200
    elif method == 'DELETE':
        return {"result": f"{tablename} deleted successfully"}, 200