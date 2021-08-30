from dataclasses import asdict
from sqlalchemy.inspection import inspect
from .returnMessages import *
from models.db import BaseModel
from models import db
from flask import json, jsonify
from sqlalchemy import Column


def getOrCreate(model: BaseModel, toInsert, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).one_or_none()
    if instance and kwargs is not None:
        return instance, False
    else:
        try:
            db.session.add(toInsert)
            db.session.commit()

            return toInsert, True
        except Exception as exc:
            print(f'exc: {exc}')
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

# returns : {"result": "{EntityType} (created|updated|deleted) succesfully" }, 200 | {"result": "<EntityType> not (created|updated|deleted)", "error": "<EntityType> already exists"}, 400
def crud(operation:str,model:BaseModel,obj,jsonReturn=False, messageReturn=False,tupleReturn=False, autoReturn=True, **kwargs):
    result = None
    opState = False
    message = None

    if operation == 'POST':
        result, opState = (getOrCreate(model=model,toInsert=obj,**kwargs))
        if autoReturn == True:
            messageReturn = True
    elif operation == 'PUT':
        result, opState = (put(model=model,toPut=obj,**kwargs))
        if autoReturn == True:
            messageReturn = True
    elif operation == 'PATCH':
        result, opState = (patch(model=model,toPatch=obj,**kwargs))
        if autoReturn == True:
            messageReturn = True
    elif operation == 'DELETE':
        opState = delete(model=model,**kwargs)
        if autoReturn == True:
            messageReturn = True
    elif operation == 'GET':
        opState = False if obj is None else True
        result = obj
        if autoReturn == True:
            jsonReturn = True

    if not opState:
        if operation == 'POST':
            message = recordAlreadyExists(model.__tablename__)
        else:
            message = recordDoesntExist(model.__tablename__)
        if tupleReturn:
            return result, opState
        else:
            return message

    if jsonReturn: # when querying
        return jsonify(result), 200
    elif messageReturn:
        message = recordCUDSuccessfully(model.__tablename__, operation)
        return message
    else:
        if result is not None:
            return result, opState
        else: 
            return opState # delete only returns True or False

def polymorphicPrimaryKeys(model): # gets the primary keys of a class
    mapper = inspect(model)
    yield from (column for column in mapper.columns if column.primary_key) 

def crudv2(key:str, model:BaseModel, body:object, method:str):
    try:
        data = json.loads(body)
        
        dictData = data[key]
        
        objs = [model(**data) for data in dictData] # instantiate the objects to operate with

        primaryKeys = [pk for pk in polymorphicPrimaryKeys(model)] # get the primary key(s) of the model
        
        filters = {f"{pk.key}": asdict(obj)[pk.key] for pk in primaryKeys
                                for obj in objs}

        print(filters)
    except Exception as exc:
        print(f'exc: {exc}')
        return provideData()
