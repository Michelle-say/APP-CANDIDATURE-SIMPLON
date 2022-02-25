from flask import Blueprint
from flask import render_template
from flask_login import login_required

profile = Blueprint("profile", __name__, static_folder="../static", template_folder="../templates")

@profile.route('/profile/')
@login_required
def profile_page():

    return render_template('profile.html')