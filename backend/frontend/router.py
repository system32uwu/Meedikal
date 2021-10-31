from flask import Blueprint, render_template
from config import Config
import os
from .app import appRouter 

frontendRouter = Blueprint('frontend', __name__, url_prefix='/') # handles /

frontendRouter.register_blueprint(appRouter)

@frontendRouter.get('/')
def index():
    return render_template('pages/landing/index.html')

@frontendRouter.get('/contact')
def contact():
    return render_template('pages/landing/contact.html')

@frontendRouter.get('/plans')
def plans():
    return render_template('pages/landing/plans.html')

@frontendRouter.get('/login')
def login():
    return render_template('pages/landing/login.html')

@frontendRouter.get('/affiliate')
def affiliate():
    return render_template('pages/landing/affiliate.html')

@frontendRouter.context_processor
def globalVars():
    return dict(company_name=Config.company_name, 
    landing_pages=Config.landing_pages,
    central_data=Config.central_data,
    plans=Config.plans,
    ENV=os.environ.get('FLASK_ENV', 'production'))