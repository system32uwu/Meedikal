from flask import Blueprint, render_template

frontendRouter = Blueprint('frontend', __name__, url_prefix='/') # handles /

@frontendRouter.route('/')
@frontendRouter.route('/<path:path>')
def frontend(path=None):
    return render_template('index.html')