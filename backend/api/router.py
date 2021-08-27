from flask import Blueprint
from .user import router as userRouter # handles /api/user
from .appointment import router as appointmentRouter # handles /api/appointment

# modular routing, instead of having all the routes in this file, I'm making multiple routers that handle each table of the database. 

apiRouter = Blueprint('api', __name__, url_prefix='/api') # handles /api

apiRouter.register_blueprint(userRouter)
apiRouter.register_blueprint(appointmentRouter) 