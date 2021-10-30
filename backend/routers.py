import os
from config import Config
from flask import Blueprint, send_file
from api.user import router as userRouter # handles /api/user
from api.appointment import router as appointmentRouter # handles /api/appointment
from api.branch import router as branchRouter # handles /api/branch
from api.auth import router as authRouter # handles /api/auth
from api.suffering import router as sufferingRouter # handles /api/suffering
from api.pagination import router as paginationRouter # handles /api/pagination
from frontend.router import frontendRouter
# modular routing, instead of having all the routes in this file, I'm making multiple routers that handle each table of the database. 

apiRouter = Blueprint('api', __name__, url_prefix='/api') # handles /api

apiRouter.register_blueprint(authRouter)
apiRouter.register_blueprint(userRouter)
apiRouter.register_blueprint(appointmentRouter) 
apiRouter.register_blueprint(branchRouter)
apiRouter.register_blueprint(sufferingRouter)
apiRouter.register_blueprint(paginationRouter)

imagesRouter = Blueprint('images', __name__, url_prefix='/images') # handles /images
@imagesRouter.get('/<resource>')
def returnResource(resource:str):
    return send_file(os.path.join(Config.UPLOAD_FOLDER, resource))