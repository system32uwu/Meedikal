from flask import Blueprint
from .user import router as userRouter # handles /api/user
from .appointment import router as appointmentRouter # handles /api/appointment
from .alert import router as alertRouter # handles /api/alert
from .vaccine import router as vaccineRouter # handles /api/vaccine
# modular routing, instead of having all the routes in this file, I'm making multiple routers that handle each table of the database. 

apiRouter = Blueprint('api', __name__, url_prefix='/api') # handles /api

apiRouter.register_blueprint(userRouter)
apiRouter.register_blueprint(appointmentRouter) 
apiRouter.register_blueprint(alertRouter) 
apiRouter.register_blueprint(vaccineRouter) 