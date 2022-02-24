from collections import UserString
from flask import render_template, redirect, url_for, flash, request

from App import db, app, mail
from datetime import date, datetime
from .models import Users, Candidacy
from .forms import Login, AddCandidacy, ModifyCandidacy, ModifyPassword, ModifyProfile, CheckEmail, CheckPwd, AddCandidacy_verif
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
import plotly.express as px
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json as js
import pandas as pd
import random
import string
import cloudinary.uploader

# from werkzeug import secure_filename

@app.route('/')
@app.route('/home')
def home_page():
    """[Allow to generate the template of home.html on home path]

    Returns:
        [str]: [home page code]
    """
    return render_template('home.html')


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


@app.route('/profile/')
@login_required
def profile_page():

    return render_template('profile.html')


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


@app.route('/stat')
@login_required
def stat_page():
    df = pd.DataFrame(Candidacy.query.join(Users).with_entities(Users.first_name,Users.last_name,Users.email_address,Candidacy.status, Candidacy.entreprise).all(),columns=["first_name","last_name","mail","status","enterprise"])
    df["full_name"] = df["first_name"] + " " + df["last_name"]
    df["alternance"] = False
    df["alternance"].loc[df["status"]=="Alternance"] = True
    fig1 = px.histogram(df["full_name"])
    graphJSON1 = js.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = px.pie(df[["mail","alternance"]].groupby(["mail"]).sum(),names="alternance")
    graphJSON2 = js.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('stat.html',graph1=graphJSON1, graph2=graphJSON2)


@app.route('/logout')
def logout_page():
    """[Allows to disconnect the user and redirect to the home page]
    """
    logout_user()
    flash('Vous êtes correctement déconnecté', category="success")
    return redirect(url_for('home_page'))


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


@app.route('/delete_candidacy', methods=['GET', 'POST'])
def delete_candidacy():
    """[Allow to delete candidacy in the BDD with the id and redirect to board page]"""

    candidacy_id = request.args.get('id')
    Candidacy.query.filter_by(id=candidacy_id).first().delete_from_db()
    flash("Candidature supprimé avec succés", category="success")

    return redirect(url_for('board_page'))


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


@app.route('/show_histogram')
def show_histogram():

        """[Allow to generate the template of statistic_hist.html to display histogram of the status of the apprenants]

    # Returns:
    #     [str]: [Show histogram page]
    # """
        # Prepare histogram of Apprenants with and witout alternance
        list_no_alternance= Users.get_list_without_alternance()
        list_with_alternance = Users.get_list_with_alternance()

        full_list_df = pd.DataFrame(columns = ['Name', 'Alternance'])

        for user_info in list_with_alternance:
            full_list_df = full_list_df.append({'Name': user_info[1]+' '+ user_info[0], 'Alternance': 'avec alternance'}, ignore_index=True)

        for user_info in list_no_alternance:
            full_list_df = full_list_df.append({'Name': user_info['first_name']+' '+ user_info['last_name'], 'Alternance': 'sans alternance'}, ignore_index=True)
        
        
        fig = px.histogram(full_list_df, x='Alternance', title = "Nombre d'apprenant en alternance", color='Alternance')
        fig.update_layout(height=400, width=600, yaxis_title="No. of Apprenants")
        plot_json1 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Prepare pie chart of Apprenants with and witout alternance
        pie_df = pd.DataFrame(columns = ['Status', 'Apprenants'])
        pie_df['Status'] = ['avec alternance', 'sans alternance']
        pie_df['Apprenants'] = [len(full_list_df.loc[full_list_df['Alternance'] =='avec alternance']), len(full_list_df.loc[full_list_df['Alternance'] =='sans alternance'])]
        

        fig = px.pie(pie_df, values='Apprenants', names='Status', title = "Pourcentage d'apprenant en alternance")
        fig.update_layout(height=500, width=500, legend_title_text='Alternance')
        plot_json2 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        kwargs = {
        'plot_json1' : plot_json1,
        'plot_json2' : plot_json2,
        }
    
        return render_template('statistic_hist.html', **kwargs)


@app.route('/user_board', methods=['GET','POST'])

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

@app.route('/show_histogram_entreprise')
def show_histogram_entreprise():
        """[Allow to generate the template of statistic_hist.html to display histogram of the status of the apprenants]

    # Returns:
    #     [str]: [Show histogram page]
    # """

        # user_name = Users.find_by_user_id(id)

        list_no_alternance= Users.get_list_without_alternance()
        list_with_alternance = Users.get_list_with_alternance()
        all_users_candidacy = Users.get_full_list()
        all_user_registered = Users.find_all_isUsers()

        get_full_name_list=[]

        for info in all_user_registered:
            get_full_name_list.append([info['id'], info['email_address']])


        entreprise_count_df = pd.DataFrame(columns = ['ID', 'No_Entreprise', 'No_Entreprise_str', 'Alternance'])

        list_email_no_alternance = []
        for user_info in list_no_alternance:
            list_email_no_alternance.append(user_info['email_address'])
        
        for info in get_full_name_list:
            activity = Candidacy.find_by_user_id(info[0])
            if info[1] in list_email_no_alternance:
                entreprise_count_df = entreprise_count_df.append({'ID':id, 'No_Entreprise': len(activity), 'No_Entreprise_str': str(len(activity)),'Alternance':'sans alternance'}, 
                    ignore_index=True)
            else:
                entreprise_count_df = entreprise_count_df.append({'ID':id, 'No_Entreprise': len(activity),'Alternance':'avec alternance'}, 
                    ignore_index=True)

        # Sort database
        entreprise_count_df = entreprise_count_df.sort_values(by=['No_Entreprise'])
        sequence_hist = [*range(entreprise_count_df['No_Entreprise'].max()+2)] 

        # Display histograme #1 
        fig = px.histogram(entreprise_count_df, x='No_Entreprise', title = 'Nombre de candidature par apprenant',color="No_Entreprise",
            category_orders={"No_Entreprise": sequence_hist})

        fig.update_layout(yaxis_title="No. des Apprenants", xaxis_title="No. des Candidature")
        fig.update_xaxes(type='category')       
        fig.update_layout(height=400, width=600, legend_title_text='No. Candidature')
        plot_json1 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Display pie chart #1 
        fig = px.pie(entreprise_count_df, names='No_Entreprise', title = 'Pourcentage de candidature par apprenant')

        fig.update_layout(height=500, width=500, legend_title_text='No. Candidature')
        plot_json2 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Display histograme #2
        fig = px.histogram(entreprise_count_df, x='No_Entreprise', title = 'Répartition des apprenants par nombre de candidature', 
            color="Alternance", barmode="group",
            category_orders={"No_Entreprise": sequence_hist})
    
        fig.update_layout(height=400, width=600, yaxis_title="No. of Apprenants", xaxis_title="No. des Apprenants")
        fig.update_xaxes(type='category')   
        plot_json3 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


        # Display histograme #4
        unique_list_df=pd.DataFrame(columns = ['User_ID', 'Entreprise', 'Ville', 'Contact_Full_Name', 'Contact_Email', 'Contact_Mobilephone'])
        full_list = Candidacy.get_all_in_list_entreprise()
        unique_list = []

        # 1cls.user_id ,2cls.entreprise,3cls.ville_entreprise, 4cls.contact_full_name, 5cls.contact_email, 6cls.contact_mobilephone

        for info in full_list:
            if info not in unique_list:
                unique_list.append(info)
                unique_list_df = unique_list_df.append({'User_ID': info[0], 'Entreprise':info[1], 'Ville': info[2], 
                    'Contact_Full_Name': info[3],'Contact_Email': info[4], 'Contact_Mobilephone': info[5]}, 
                    ignore_index=True)

        
        fig = px.histogram(unique_list_df, x='Ville', title = 'Répartition géographique des candidatures',color="Ville")
        #     # category_orders={"No_Entreprise": sequence_hist})

        fig.update_layout(yaxis_title="No. des Entreprise")
        fig.update_xaxes(type='category')       
        fig.update_layout(height=400, width=600)
        plot_json4 = js.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)        

        kwargs = {
        'plot_json1' : plot_json1,
        'plot_json2' : plot_json2,
        'plot_json3' : plot_json3,
        'plot_json4' : plot_json4
        }
    
        return render_template('statistic_hist_entreprise.html', **kwargs)


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

@app.route('/checkemail',methods=["POST","GET"])
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


@app.route("/new_password/<string:hashCode>",methods=["GET","POST"])
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

