from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import Users
from ..forms import CheckEmail, CheckPwd
from werkzeug.security import generate_password_hash
import random
import string
from flask_mail import Message
from .. import db, mail

checkemail = Blueprint("checkemail", __name__, static_folder="../static", template_folder="../templates")

@checkemail.route('/checkemail',methods=["POST","GET"])
def check_email_page():
    form = CheckEmail()
    check = Users.query.filter_by(email_address=form.email.data).first()

    if check:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'candy59.app@gmail.com', recipients = [form.email.data])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n https://candi-app1.herokuapp.com/new_password/" + check.hashCode
            mail.send(msg)
            flash('Si l\'adresse Email est associé à un compte, un message vous a été envoyé pour reset votre password', category='warning' )
            return redirect(url_for('login_page'))
    return render_template('check_email.html', form=form)


@checkemail.route("/new_password/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    form = CheckPwd()
    check = Users.query.filter_by(hashCode=hashCode).first() 
    if check:
        if request.method == 'POST':
            passw = form.passw.data
            cpassw = form.cpassw.data
            if passw == cpassw:
                check.password_hash = generate_password_hash(passw, method='sha256')
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('login_page'))
            else:
                flash('error')
                return render_template('new_password.html', form=form)
        else:
            return render_template('new_password.html', form=form)
    else:
        return render_template('new_password.html', form=form)