def recordDoesntExists(record:str):
    return f"{record} doesn't exist", 400

def recordAlreadyExists(record:str):
    return f"{record} doesn't exist", 400

def notFound(record:str):
    return f"no {record} was found", 400

def provideData():
    return "provide data", 400

def recordCUDSuccessfully(record:str,create=False, update=False, delete=False):
    if create:
        return f"{record} created successfully", 200
    elif update:
        return f"{record} updated successfully", 200
    else:
        return f"{record} deleted successfully", 200