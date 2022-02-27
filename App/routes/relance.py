from flask import Blueprint
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request
from ..models import Candidacy
from ..forms import AddCandidacy, AddCandidacy_verif, ModifyCandidacy
from datetime import date
from App import db 


relance = Blueprint("relance", __name__, static_folder="../static", template_folder="../templates")

# 3 Fonctions de relances
def date_relance(date):
    annee = int(date.replace('-','')[0:4])
    mois = int(date.replace('-','')[4:6])
    jours = int(date.replace('-','')[6:])
    max_mois = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    max_current_mois = max_mois[mois]
    
    math_jour = jours + 7
    
    # Compare if 7 days more reached the end of mounth  
    if math_jour > max_current_mois :
        if mois == 12 :
            annee += 1 
            mois = 1 
            math_jour -= max_current_mois
        else:
            mois += 1 
            math_jour -= max_current_mois
        
    # For the correct format print
    if mois < 10 :
        mois = "0" + str(mois)
    if math_jour < 10 :
        math_jour = "0" + str(math_jour)
        
    result = str(annee) + "-" + str(mois) + "-" + str(math_jour)
    return result

def diff_date(date_to_compare ):
    
    date_now = str(date.today())
    annee_1 = date_now[0:4]
    mois_1 = date_now[5:7]
    jours_1 = date_now[8:]
    
    annee_2 = date_to_compare[0:4]
    mois_2 = date_to_compare[5:7]
    jours_2 = date_to_compare[8:]
    if (annee_1 >= annee_2 ) and (mois_1 > mois_2 ) :
        return True
    elif (annee_1 >= annee_2 ) and (mois_1 >= mois_2) and (jours_1 > jours_2):
        return True 
    else:
        return False

def count_alertes():
    
    alertes = 0 
    this_user = Candidacy.find_by_user_id_relance(Candidacy, current_user.id)
    for i in this_user :
        if i['relance'] == False :
            if i['status'] == 'En cours': 
                if diff_date(date_relance(i['date'])):
                    alertes += 1
    return alertes


# Route relance 
@relance.route('/relance')
def relance_page():
    header = ['entreprise','contact_full_name','contact_email', 'contact_mobilephone' ,'Date de candidature', 'A relancer dès le', 'Candidature relancée']
    body = ['entreprise', 'contact_full_name', 'contact_email', 'contact_mobilephone' , 'date', 'relance','date_last_relance' ]
    
    
    adresse = current_user.email_address 
    user_candidacy = Candidacy.find_by_user_id_relance(Candidacy, current_user.id)
    
    
    return render_template('relance.html', title = header, user_candidacy=user_candidacy, math_relance=date_relance, body = body, alertes = count_alertes())

