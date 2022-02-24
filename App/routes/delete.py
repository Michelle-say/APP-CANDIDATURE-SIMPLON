from imports import *

@app.route('/delete_candidacy', methods=['GET', 'POST'])
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimé avec succés", category="success")

    return redirect(url_for('board_page'))