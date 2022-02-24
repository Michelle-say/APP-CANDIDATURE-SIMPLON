from imports import *

@app.route('/candidature', methods=['GET', 'POST'])
def add_candidature():
    """[Allow to generate the template of add_candidacy.html on candidacy path to add candidacy in the BDD if validate and redirect to the board page when finish]

    Returns:
        [str]: [Candidacy code page]
    """
    form = AddCandidacy()

    if form.validate_on_submit():
        if form.entreprise.data.startswith('- ') == False:
            entreprise_similaire = Candidacy.check_entreprise_exist(form.entreprise.data)

            if entreprise_similaire != []:
                entreprise_similaire.append('- ' + form.entreprise.data)
                #entreprise_similaire.append('')
                form = AddCandidacy_verif()
                form.entreprise.choices = entreprise_similaire
                flash('Merci de sélectionner l\'ortographe du nom de l\'entreprise', category='danger' )
                return render_template('add_candidacy.html', form=form, Date_Today=date.today())

        if form.entreprise.data.startswith('- '): form.entreprise.data = form.entreprise.data[2:]
        Candidacy(user_id = current_user.id, 
            status = form.status.data,
            comment = form.comment.data,
            entreprise = form.entreprise.data,
            ville_entreprise = form.ville_entreprise.data,
            contact_full_name = form.contact_full_name.data,
            contact_email = form.contact_email.data,
            contact_mobilephone = form.contact_mobilephone.data,
            date =form.date.data).save_to_db()

        flash('Nouvelle Candidature ajouté ', category='success')
        return redirect(url_for('board_page'))
    return render_template('add_candidacy.html', form=form, Date_Today=date.today())