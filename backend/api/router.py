from flask import Blueprint
from .user import router as userRouter # handles /api/user
from .appointment import router as appointmentRouter # handles /api/appointment
from .branch import router as branchRouter # handles /api/branch
# modular routing, instead of having all the routes in this file, I'm making multiple routers that handle each table of the database. 

from util.returnMessages import *
from util.createDb import getDb

apiRouter = Blueprint('api', __name__, url_prefix='/api') # handles /api

apiRouter.register_blueprint(userRouter)
apiRouter.register_blueprint(appointmentRouter) 
apiRouter.register_blueprint(branchRouter)

@apiRouter.errorhandler(Exception) # TODO: Handle errors better
def handle_exception(e:Exception):
    _e = repr(e)
    print(_e)
    getDb().rollback()
    if "object is not subscriptable" or "JSONDecodeError" in _e:
        return provideData()
    elif "object has no attribute" in _e: # does that really mean it doesn't exist?
        return recordDoesntExist()
    elif "UNIQUE" in _e:
        return recordAlreadyExists()
    else:
        return {"error": repr(_e)}, 400