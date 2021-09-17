from flask import Blueprint, render_template

frontendRouter = Blueprint('frontend', __name__, url_prefix='/') # handles /

@frontendRouter.get('') # @reach/router will take care of the rest of routing.
def frontend():
    return render_template('index.html')