from flask import Blueprint
from flask import render_template

home = Blueprint("home", __name__, static_folder="../static", template_folder="../templates/")

@home.route('/')
@home.route('/home')
def home_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    
    return render_template('home.html')  