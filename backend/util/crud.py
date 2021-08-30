from dataclasses import asdict
from flask.wrappers import Request
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.expression import text
from .returnMessages import *
from models.db import BaseModel
from models import db
from flask import json, jsonify

def get(model:BaseModel,filterStr:str):
    instances = db.session.query(model).filter(filterStr).all()
    if len(instances) < 1:
        return instances, False
    else:
        return instances, True

def getOrCreate(model: BaseModel, toInsert, filterStr:str):
    instances, status = (get(model,filterStr))

    if status: # already exists, won't create
        return instances, False
    else:
        try:
            db.session.add(toInsert)
            db.session.commit()
            return toInsert, True
        except Exception:
            db.session.rollback()
            return instances, False

def put(model:BaseModel, toPut, filterStr:str): # PUT replaces the entire record
    instances, status = (get(model,filterStr))
    
    if not status: # can't update if record doesn't exist
        return instances, False
    else:
        try:
            for instance in instances:
                for key, value in dict(toPut).items():
                    if key != '_sa_instance_state':
                        setattr(instance,key,value)

            db.session.commit()
            return instances, True
        except Exception:
            db.session.rollback()
            return instances, False

def patch(model:BaseModel, toPatch, filterStr:str): # PATCH updates the provided values
    instances, status = (get(model,filterStr))
    
    if not status: # can't update if record doesn't exist
        return instances, False
    else:
        try:
            for instance in instances:
                for key, value in dict(toPatch).items():
                    if key != '_sa_instance_state' and value is not None:
                        setattr(instance,key,value)

            db.session.commit()
            return instances, True
        except Exception: 
            db.session.rollback()
            return instances, False

def delete(model:BaseModel,filterStr:str): # DELETE by the given filters
    instances, status = (get(model,filterStr))
    
    if not status: # can't delete if record doesn't exist
        return False
    else:
        try:
            for instance in instances:
                instance.delete()
            return True
        except Exception: 
            db.session.rollback()
            return False

def getPrimaryKeys(model): # gets the primary key(s) of a class
    mapper = inspect(model)
    yield from (column for column in mapper.columns if column.primary_key) 

def crudv2(key:str, model:BaseModel, request:Request, operator='AND',
           jsonReturn=False, messageReturn=False,tupleReturn=False, autoReturn=True):
    
    result = None
    opState = None
    message = None

    try:
        data = json.loads(request.data)

        dictData = data[key]

        if not isinstance(dictData, list): # convert to list in order to make things easier
            dictData = [dictData]
        
        objs = [model(**data) for data in dictData] # instantiate the objects to operate with

        primaryKeys = [pk for pk in getPrimaryKeys(model)] # get the primary key(s) of the model
             
        # make if statements with the possible requests methods, pass the filterStr

        for obj in objs:

            filters = {f"{pk.key}": asdict(obj)[pk.key] for pk in primaryKeys
                       if asdict(obj)[pk.key] is not None}
            filterStr = ''

            for key,value in filters.items():
                if len(filterStr) > 0:
                    filterStr += operator
                filterStr += f" {key} = {value} "

            filterStr = text(filterStr)

            if request.method == 'POST':
                result, opState = (getOrCreate(model=model,toInsert=obj,filter=filterStr))
            elif request.method == 'PUT':
                result, opState = (put(model=model,toPut=obj,filter=filterStr))
            elif request.method == 'PATCH':
                result, opState = (patch(model=model,toPatch=obj,filter=filterStr))
            elif request.method == 'DELETE':
                opState = delete(model=model,filter=filterStr)
            elif request.method == 'GET':
                result, opState = get(model,filterStr)

        if autoReturn:
            if request.method == 'GET':
                jsonReturn = True
            else:
                messageReturn = True
        
        if not opState:
            if request.method == 'POST':
                message = recordAlreadyExists(model.__tablename__)
            else:
                message = recordDoesntExist(model.__tablename__)

        if jsonReturn:
            return jsonify([asdict(res) for res in result]), 200
        elif messageReturn:
            if message is None:
                message = recordCUDSuccessfully(model.__tablename__, request.method)
            return message
        elif tupleReturn:
            return result,opState
        else:
            if result is None:
                return opState
        # return jsonify(result), 200

    except Exception as exc:
        print(f'exc: {exc}')
        return provideData()
