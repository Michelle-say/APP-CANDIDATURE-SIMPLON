from imports import *

@app.route('/list_with_alternance', methods=['GET', 'POST'])
def show_list_with_alternance():
    """[Allow to generate the template of list_with_alternance.html to display the list of students that have found an alternance]

# Returns:
#     [str]: [List with alternance page]
# """
    attributs = ["user_fisrt_name", "user_last_name",
                 'contact_email', 'status', 'entreprise']
    return render_template('list_with_alternance.html', lenght=len(attributs), title=attributs, user_candidacy=Users.get_list_with_alternance())


@app.route('/list_without_alternance', methods=['GET', 'POST'])
def show_list_without_alternance():
    """[Allow to generate the template of list_with_alternance.html to display the list of students that have yet found an alternance]

# Returns:
#     [str]: [List without alternance page]
# """
    attributs = ["user_fisrt_name",
                 "user_last_name", 'contact_email', 'action']

    # add action to view progress
    return render_template('list_without_alternance.html', lenght=len(attributs), title=attributs, user_candidacy=Users.get_list_without_alternance())

@app.route('/list_entreprise', methods=['GET','POST'])

def list_entreprise_page():
    """[Allow to generate the template of list_entreprise.html to display the contact information of companies]

    Returns:
        [str]: [Show list_entreprise.html]
    """
    attributs = ["Entreprise","ville",'contact_full_name', 'contact_email','contact_mobilephone']

    # Add only unique items:
    unique_list=[]
    full_list = Candidacy.get_all_in_list_entreprise()

    for info in full_list:
        if info not in unique_list:
            unique_list.append(info)
            
    return render_template('list_entreprise.html', lenght = len(attributs), title = attributs, user_candidacy=unique_list)