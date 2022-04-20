from unicodedata import category
from flask import Blueprint,render_template, redirect, url_for, flash, request, session
from ..models import Users
from ..forms import Login, ModifyPassword, ModifyProfile, AddUser
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from flask_dance.contrib.github import make_github_blueprint, github
from .. import db, oauth

import cloudinary.uploader
import os

auth = Blueprint("auth", __name__, static_folder="../static", template_folder="../templates")


@auth.route('/add_user', methods= ['GET', 'POST'])
def add_user():
    """[To add an user to the database]
    Returns:
        [str]: [User code page]
    """

    form = AddUser()        
    if form.validate_on_submit():
        user = Users.query.filter_by(email_address=form.email_address.data).first()
        if user :
            flash("L'adresse email existe déjà. Merci d'en choisir une nouvelle", category='danger')
        elif form.password_hash.data != form.password_hash2.data:
            flash("Veuillez entrer deux fois le même mot de passe", category='danger')
        else:
            Users(last_name = form.last_name.data, first_name = form.first_name.data, email_address = form.email_address.data, password_hash = generate_password_hash(form.password_hash.data, method='sha256'), promo_id = 1).save_to_db()
            flash('Nouvel utilisateur ajouté ', category='secondary')
            return redirect(url_for('auth.login_page'))
    return render_template('add_user.html', form=form)



@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    """[Allow to ask login and generate the template of login.html on login path]

    Returns:
        [str]: [login page code]
    """
    form = Login()
    if form.validate_on_submit():
        user = Users.query.filter_by(email_address=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}", category="success")
            return redirect(url_for('candidature.board_page'))
        else:
            flash('Adresse email ou mot de passe invalide', category="danger")
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout_page():
    """[Allows to disconnect the user and redirect to the home page]
    """
    logout_user()
    flash('Vous êtes correctement déconnecté', category="success")
    return redirect(url_for('home.home_page'))

@auth.route('/modify_password', methods=['GET', 'POST'])
@login_required
def modify_password():
    """[Allow to generate the template of modify_password.html on modify_password path to modify password in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify password code page]
    """
    form = ModifyPassword()
    if form.validate_on_submit():
        if current_user.email_address == form.email.data and check_password_hash(current_user.password_hash, form.current_password.data):
            current_user.password_hash = generate_password_hash(
                form.new_password.data, method='sha256')
            db.session.add(current_user)
            db.session.commit()

            flash(f"Votre mot de passe a été modifié", category="success")
            return redirect(url_for('candidature.board_page'))
        else:
            flash('Adresse email ou mot de passe invalide', category="danger")
    return render_template('modify_password.html', form=form)

@auth.route('/modify_profile/', methods=['GET', 'POST'])
@login_required
def modify_profile_page():
    form = ModifyProfile()

    if form.validate_on_submit():
        current_user.last_name = form.last_name.data
        current_user.first_name = form.first_name.data
        current_user.email_address = form.email_address.data
        current_user.telephone_number = form.telephone_number.data
        current_user.filename = None
        
        file_to_upload = request.files.get('profil')
        if file_to_upload:
            print('file to upload')
            upload_result = cloudinary.uploader.upload(file_to_upload)
            current_user.filename = upload_result['secure_url']

        db.session.add(current_user)
        db.session.commit()
        flash(f"Votre profil a été modifié avec succès.", category="success")

        return redirect(url_for('profile.profile_page'))

    return render_template('modify_profile.html', form=form, current_user=current_user)

@auth.route('/google/')
def google():
   
    # Google Oauth Config
    # Get client_id and client_secret from enviroment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
     
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    # Redirect to google_auth function
    redirect_uri = url_for('auth.google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
  
@auth.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    user1 = Users.query.filter_by(email_address=user.email).first()
    if user1 and user.email_verified == True:
            login_user(user1)
    print(" Google User ", user1)
    return redirect('/')

@auth.route('/twitter/')
def twitter():
   
    # Twitter Oauth Config
    TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID')
    TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET')
    oauth.register(
        name='twitter',
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.twitter.com/1.1/',
        client_kwargs=None,
    )
    redirect_uri = url_for('twitter_auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)
 
@auth.route('/twitter/auth/')
def twitter_auth():
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    profile = resp.json()
    print(" Twitter User", profile)
    return redirect('/')
 
@auth.route('/facebook/')
def facebook():
   
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('auth.facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)
 
@auth.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    return redirect('/')


