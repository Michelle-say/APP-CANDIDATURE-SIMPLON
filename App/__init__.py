import os
import cloudinary
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_login import LoginManager
from flask_mail import Mail


load_dotenv(override=True)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_PORT'] = 465

    cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), api_secret=os.getenv('API_SECRET'))

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    mail.init_app(app)

    from . import models
    
    from .routes import auth
    from .routes import candidature
    from .routes import checkemail
    from .routes import histogram
    from .routes import home
    from .routes import list
    from .routes import profile
    from .routes import stat
    from .routes import userboard
    
	# blueprint for auth routes in our app
    app.register_blueprint(auth.auth)
    app.register_blueprint(candidature.candidature)
    app.register_blueprint(checkemail.checkemail)
    app.register_blueprint(histogram.histogram)
    app.register_blueprint(home.home)
    app.register_blueprint(list.list)
    app.register_blueprint(profile.profile)
    app.register_blueprint(stat.stat)
    app.register_blueprint(userboard.userboard)
    
    return app

login_manager = LoginManager()
mail = Mail()
app = create_app()