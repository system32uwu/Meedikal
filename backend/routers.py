import os
from config import Config
from flask import Blueprint, send_file, render_template
from api.user import router as userRouter # handles /api/user
from api.appointment import router as appointmentRouter # handles /api/appointment
from api.branch import router as branchRouter # handles /api/branch
from api.auth import router as authRouter # handles /api/auth

from frontend.app import appRouter # handles /app
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

frontendRouter.register_blueprint(appRouter)

@frontendRouter.get('/')
def index():
    return render_template('pages/landing/index.html')

class Page:
    route: str
    name: str

    def __init__(self, route, name) -> None:
        self.route = route
        self.name = name

@frontendRouter.context_processor
def globalVars():
    return dict(company_name='Healthcare Company', 
    landing_pages=[Page('/', 'Home'), Page('/contact', 'Contact'), Page('/plans', 'Plans')])