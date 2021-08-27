def recordDoesntExists(tablename:str):
    return {"error": f"{tablename} doesn't exists"}, 400

def recordAlreadyExists(tablename:str):
    return {"error": f"{tablename} already exists"}, 400

def notFound(tablename:str):
    return {"error": f"no {tablename} was found"}, 400

def provideData():
    return {"error": "no data was provided"}, 400

def recordCUDSuccessfully(tablename:str,create=False, update=False, delete=False):
    if create:
        return {"result": f"{tablename} created successfully"}, 200
    elif update:
        return {"result": f"{tablename} updated successfully"}, 200
    elif delete:
        return {"result": f"{tablename} deleted successfully"}, 200