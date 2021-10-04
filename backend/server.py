import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig
from routers import apiRouter, frontendRouter, imagesRouter
from util.JSONEncoder import JsonExtendEncoder
import errorhandlers

load_dotenv()

app = Flask(__name__, static_folder='build/static', template_folder='build')
CORS(app, supports_credentials=True)

if os.environ.get('FLASK_ENV', None) == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
# --- CUSTOM ENCODER (used to encode dates)
app.json_encoder = JsonExtendEncoder

# --- MAIN ROUTERS
app.register_blueprint(apiRouter) # api
app.register_blueprint(frontendRouter) # frontend
app.register_blueprint(imagesRouter) # /images
# --- MAIN ROUTERS

if __name__ == '__main__':
    try: # create the uploads folder if it doesn't exist
        os.makedirs(DevelopmentConfig.UPLOAD_FOLDER)
    except:
        pass
    finally:
        app.run()