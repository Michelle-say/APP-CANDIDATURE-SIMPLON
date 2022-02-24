from imports import *

@app.route('/board', methods=['GET', 'POST'])
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
        return render_template('board.html', lenght=len(usercandidacy_attributs), title=usercandidacy_attributs, user_candidacy=Candidacy.find_by_user_id(current_user.id))
