def recordDoesntExist(tablename:str):
    return {"error": f"{tablename} doesn't exist"}, 400

def recordAlreadyExists(tablename:str, extraMessage=None):
    return {"error": f"{tablename} already exists",
            "extraMessage": extraMessage}, 400

def provideData():
    return {"error": "no data was provided or it was invalid"}, 412

def recordCUDSuccessfully(success:bool):
    return {"result": True if success else False}, 200 if success else 400