from flask import Blueprint
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request
from ..models import Candidacy
from ..forms import AddCandidacy, AddCandidacy_verif, ModifyCandidacy
from datetime import date
from App import db 

candidature = Blueprint("candidature", __name__, static_folder="../static", template_folder="../templates")

@candidature.route('/board', methods=['GET', 'POST'])
@login_required
def board_page():
    
    
    """[Allow to generate the template of board.html on board path, if user is authenticated else return on login]

    Returns:
        [str]: [board page code different if the user is admin or not]
    """
    admin_candidacy_attributs = ["Nom", 'entreprise',
                                 'Nom du contact', 'Email du contact', 'Telephone du contact', 'date', 'statut']
    usercandidacy_attributs = ['Entreprise', 'Ville entreprise', 'Nom du contact',
                               'Email du contact', 'Telephone du contact', 'date', 'statut', 'commentaire']

    if (current_user.is_admin == True):
        return render_template('board.html', lenght=len(admin_candidacy_attributs), title=admin_candidacy_attributs, user_candidacy=Candidacy.get_all_in_list_with_user_name())
    else:
        return render_template('board.html', lenght=len(usercandidacy_attributs), title=usercandidacy_attributs, user_candidacy=Candidacy.find_by_user_id(Candidacy, current_user.id))

@candidature.route('/candidature', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('candidature.board_page'))
    return render_template('add_candidacy.html', form=form, Date_Today=date.today())

@candidature.route('/modify_candidacy', methods=['GET', 'POST'])
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
            candidacy.date_last_relance = date.today()
            candidacy.relance = form.relance.data
            db.session.commit()

            flash(f"La candidature a bien été modifié", category="success")
            return redirect(url_for('candidature.board_page'))
        else:
            flash('Something goes wrong', category="danger")
    form.comment.data = candidacy.comment
    return render_template('modify_candidacy.html', form=form, candidacy=candidacy.json())

@candidature.route('/delete_candidacy', methods=['GET', 'POST'])
@login_required
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimé avec succés", category="success")

    return redirect(url_for('candidature.board_page'))