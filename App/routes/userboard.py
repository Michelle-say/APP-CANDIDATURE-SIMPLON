from flask import Blueprint
from flask import render_template, request
from flask_login import login_required
from ..models import Users, Candidacy

userboard = Blueprint("userboard", __name__, static_folder="../static", template_folder="../templates")

@userboard.route('/user_board', methods=['GET','POST'])
@login_required
def user_board_page():
    """[Allow to generate the template of board.html on board path, if user is authenticated else return on login]

    Returns:
        [str]: [board page code different if the user is admin or not]
    """

    id = request.args.get('id')
    user_name = Users.find_by_user_id(id)

    user_name =user_name[0]['first_name'] + ' ' + user_name[0]['last_name']

    usercandidacy_attributs = ['entreprise','ville','contact_full_name','contact_email', 'contact_mobilephone' ,'date','status', 'comment']

    return render_template('user_board.html', lenght=len(usercandidacy_attributs), user_name=user_name, title=usercandidacy_attributs, user_candidacy=Candidacy.find_by_user_id(id))
