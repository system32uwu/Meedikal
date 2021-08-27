from models.db import BaseModel
from models import db

def getOrCreate(model: BaseModel, toInsert, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance, False
    else:
        try:
            db.session.add(toInsert)
            db.session.commit()

            return toInsert, True
        except Exception:
            db.session.rollback()
            instance = db.session.query(model).filter_by(**kwargs).one()

            return instance, False

def put(model:BaseModel, toPut, **kwargs): # PUT replaces the entire record
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    
    if not instance:
        return instance, False
    else:
        try:
            for key, value in dict(toPut).items():
                if key != '_sa_instance_state':
                    setattr(instance,key,value)

            db.session.commit()

            return instance, True
        except Exception:
            db.session.rollback()
            instance = db.session.query(model).filter_by(**kwargs).one()
            return instance, False

def patch(model:BaseModel, toPatch, **kwargs): # PATCH updates the provided values
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    
    if not instance:
        return instance, False
    else:
        try:
            for key, value in dict(toPatch).items():
                if key != '_sa_instance_state' and value is not None:
                    setattr(instance,key,value)

            db.session.commit()

            return instance, True
        except Exception: 
            db.session.rollback()
            instance = db.session.query(model).filter_by(**kwargs).one()
            return instance, False

def delete(model:BaseModel, **kwargs): # DELETE by the given filters
    instances = db.session.query(model).filter_by(**kwargs).all()
    
    if not instances:
        return False
    else:
        try:
            for instance in instances:
                instance.delete()

            return True
        except Exception: 
            db.session.rollback()
            return False

def crud(operation:str,model:BaseModel,obj,**kwargs):
    if operation == 'POST':
        return getOrCreate(model=model,toInsert=obj,**kwargs)
    elif operation == 'PUT':
        return put(model=model,toPut=obj,**kwargs)
    elif operation == 'PATCH':
        return patch(model=model,toPatch=obj,**kwargs)
    elif operation == 'DELETE':
        return delete(model=model,**kwargs)

# returns : {"result": "<EntityType> (created|updated|deleted) succesfully" }, 200 | {"result": "<EntityType> not (created|updated|deleted)", "error": "<EntityType> already exists"}, 400 
def crudReturn(operation:str, model:BaseModel): 
    pass
