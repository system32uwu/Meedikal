import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig
from routers import apiRouter, frontendRouter, imagesRouter
from util.JSONEncoder import JsonExtendEncoder
import errorhandlers
import mimetypes 

load_dotenv() # load .env file

def create_app() -> Flask:

    app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
    CORS(app, supports_credentials=True) # apply CORS to flask app

    if os.environ.get('FLASK_ENV', None) == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    # --- CUSTOM ENCODER (used to encode dates)
    app.json_encoder = JsonExtendEncoder

    # --- MAIN ROUTERS
    app.register_blueprint(apiRouter) # /api
    app.register_blueprint(frontendRouter) # /
    app.register_blueprint(imagesRouter) # /images
    # --- MAIN ROUTERS
    
    try: # create the uploads folder if it doesn't exist
        os.makedirs(DevelopmentConfig.UPLOAD_FOLDER)
    except:
        pass

    # solve mime type bugs when using javascript files in templates
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/javascript', '.js')
    
    return app

if __name__ == '__main__':
    create_app().run()