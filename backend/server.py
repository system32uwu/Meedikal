import os
from flask import Flask, redirect
from flask_cors import CORS
from config import DevelopmentConfig
from routers import apiRouter, frontendRouter, imagesRouter
import errorhandlers
from util.JSONEncoder import JsonExtendEncoder
from util.errors import MissingCookieError

app = Flask(__name__, static_folder='build/static', template_folder='build')

app.config.from_object(DevelopmentConfig)

# --- CUSTOM ENCODER (used to encode dates)
app.json_encoder = JsonExtendEncoder

# --- MAIN ROUTERS
app.register_blueprint(apiRouter) # api
app.register_blueprint(frontendRouter) # frontend
app.register_blueprint(imagesRouter) # /images
# --- MAIN ROUTERS

@app.errorhandler(MissingCookieError)
def missingCookieError(e):
    return redirect('/app/login')
    # return genericErrorReturn('Not authenticated (missing cookie)', code=401)

if __name__ == '__main__':
    try: # create the uploads folder if it doesn't exist
        os.makedirs(DevelopmentConfig.UPLOAD_FOLDER)
    except:
        pass
    finally:
        CORS(app, supports_credentials=True)    
        app.run()