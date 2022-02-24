from imports import *

@app.route('/modify_candidacy', methods=['GET', 'POST'])
@login_required
def modify_candidacy():
    """[Allow to generate the template of modify_candidacy.html on modify_candidacy path to modify candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [modify candidacy code page]
    """
    form = ModifyCandidacy()
    candidacy_id = request.args.get('id')
    candidacy = Candidacy.query.filter_by(id=candidacy_id).first()
    if form.validate_on_submit():

        if candidacy:
            candidacy.entreprise = form.entreprise.data
            candidacy.ville_entreprise = form.ville_entreprise.data
            candidacy.contact_full_name = form.contact_full_name.data
            candidacy.contact_email = form.contact_email.data
            candidacy.contact_mobilephone = form.contact_mobilephone.data
            candidacy.status = form.status.data
            candidacy.date = form.date.data
            candidacy.comment = form.comment.data
            db.session.commit()

            flash(f"La candidature a bien été modifié", category="success")
            return redirect(url_for('board_page'))
        else:
            flash('Something goes wrong', category="danger")
    form.comment.data = candidacy.comment
    print(candidacy.json())
    return render_template('modify_candidacy.html', form=form, candidacy=candidacy.json())


@app.route('/modify_password', methods=['GET', 'POST'])
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
            return redirect(url_for('board_page'))
        else:
            flash('Adresse email ou mot de passe invalide', category="danger")
    return render_template('modify_password.html', form=form)


@app.route('/modify_profile/', methods=['GET', 'POST'])
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
            app.logger.info(upload_result)
            current_user.filename = upload_result['secure_url']

        db.session.add(current_user)
        db.session.commit()
        flash(f"Votre profil a été modifié avec succès.", category="success")

        return redirect(url_for('profile_page'))

    return render_template('modify_profile.html', form=form, current_user=current_user)