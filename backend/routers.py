import os

from config import Config
from flask import Blueprint, render_template
from flask import send_file, request, redirect
from middleware.authGuard import requiresAuth
from api.user import router as userRouter # handles /api/user
from api.appointment import router as appointmentRouter # handles /api/appointment
from api.branch import router as branchRouter # handles /api/branch
from api.auth import router as authRouter # handles /api/auth
# modular routing, instead of having all the routes in this file, I'm making multiple routers that handle each table of the database. 

apiRouter = Blueprint('api', __name__, url_prefix='/api') # handles /api

apiRouter.register_blueprint(authRouter)
apiRouter.register_blueprint(userRouter)
apiRouter.register_blueprint(appointmentRouter) 
apiRouter.register_blueprint(branchRouter)

imagesRouter = Blueprint('images', __name__, url_prefix='/images') # handles /images
@imagesRouter.get('/<resource>')
def returnResource(resource:str):
    return send_file(os.path.join(Config.UPLOAD_FOLDER, resource))

frontendRouter = Blueprint('frontend', __name__, url_prefix='/') # handles /

@frontendRouter.route('app/login')
def loginRoute():
    return render_template('index.html')

@frontendRouter.route('app/<path:path>')
@requiresAuth
def appRoute(path=None, ci:int=None):
    return render_template('index.html')

@frontendRouter.route('')
@frontendRouter.route('/<path:path>')
def frontend(path=None):
    return render_template('index.html')