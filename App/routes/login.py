from imports import *

@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide', category="danger")
    return render_template('login.html', form=form)