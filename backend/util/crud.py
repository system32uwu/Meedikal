from models import db

def get_or_create(model, toInsert, **kwargs):
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

def put(model, toPut, **kwargs): # PUT replaces the entire record
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

def patch(model, toPatch, **kwargs): # PATCH updates the provided values
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

def delete(model, **kwargs): # DELETE by the given filters
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