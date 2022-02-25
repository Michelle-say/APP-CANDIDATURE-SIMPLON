from flask import Blueprint,render_template, redirect, url_for, flash, request
from ..models import Users
from ..forms import Login, ModifyPassword, ModifyProfile
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .. import db

import cloudinary.uploader

auth = Blueprint("auth", __name__, static_folder="../static", template_folder="../templates")

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
            flash(
                f"Vous êtes connecté en tant que : {user.first_name} {user.last_name}", category="success")
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