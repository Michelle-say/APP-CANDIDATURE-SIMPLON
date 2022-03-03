from logging import PlaceHolder
from flask_wtf import FlaskForm

from wtforms import PasswordField, EmailField, SubmitField, StringField, TextAreaField, FileField, BooleanField
from wtforms.fields import DateField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from .models import Users


class Login(FlaskForm):
    """[Form to login]
    """
    email = EmailField(label="Adresse mail:", validators=[DataRequired()])
    password = PasswordField(label="Mot de passe:",
                             validators=[DataRequired()])
    submit = SubmitField(label="Se connecter")


class AddCandidacy(FlaskForm):
    """[Form to add candidacy]
    """
    entreprise = StringField(label='Entreprise', validators=[DataRequired(),Length(max=50)])
    ville_entreprise = StringField(label='Ville de l\'entreprise', validators=[DataRequired(),Length(max=50)])
    contact_full_name = StringField(label='Nom du contact', validators=[DataRequired(),Length(max=50)])
    contact_email = EmailField(label='Email du contact', validators=[Length(max=50)])
    contact_mobilephone = StringField(label='Téléphone du contact',validators=[Length(max=20)])
    comment = TextAreaField(label='Commentaire',validators=[Length(max=500)])
    status = SelectField(label='Statut',choices=[
                         'En cours', 'Refusée', 'Acceptée en alternance', 'Besoin d\'aide'], validators=[DataRequired()])
    date = DateField(label='Date de la candidature',validators=[DataRequired()],format='%Y-%m-%d')
    print("En cours d'ajout")
    submit = SubmitField(label='Ajouter')


class AddCandidacy_verif(FlaskForm):
    """[Form to add candidacy]
    """
    entreprise = SelectField(label='Liste des entreprises', validators=[DataRequired(),Length(max=50)])
    ville_entreprise = StringField(label='Ville de l\'entreprise', validators=[DataRequired(),Length(max=50)])
    contact_full_name = StringField(label='Nom du contact', validators=[DataRequired(),Length(max=50)])
    contact_email = EmailField(label='Email du contact', validators=[Length(max=50)])
    contact_mobilephone = StringField(label='Téléphone du contact',validators=[Length(max=20)])
    comment = TextAreaField(label='Commentaire',validators=[Length(max=500)])
    status = SelectField(label='Statut',choices=[
                         'En cours', 'Refusée', 'Acceptée en aleternance', 'Besoin d\'aide'], validators=[DataRequired()])
    date = DateField(label='Date de la candidature',validators=[DataRequired()],format='%Y-%m-%d')
    print("En cours d'ajout")
    submit = SubmitField(label='Ajouter')


class ModifyPassword(FlaskForm):
    """[Form to modify password]

    """
    email = EmailField(label="Adresse mail:", validators=[DataRequired()])
    current_password = PasswordField(
        label="Mot de passe actuel:", validators=[DataRequired()])
    new_password = PasswordField(
        label="Nouveau mot de passe:", validators=[DataRequired()])

    submit = SubmitField(label="Valider")


class ModifyCandidacy(FlaskForm):
    """[form to modify candidacy]
    """

    entreprise = StringField(label='Entreprise', validators=[DataRequired(),Length(max=50)])
    ville_entreprise = StringField(
        label='Ville de l\'entreprise', validators=[DataRequired(),Length(max=50)])
    contact_full_name = StringField(
        label='Nom du contact', validators=[DataRequired(),Length(max=50)])
    contact_email = StringField(
        label='Email du contact', validators=[DataRequired(),Length(max=50)])
    contact_mobilephone = StringField(label='Téléphone du contact', validators=[DataRequired(),Length(max=50)])
    status = SelectField(label='Statut', choices=[
                         'En cours', 'Refusée', 'Accepté en aleternance', 'Besoin d\'aide'], validators=[DataRequired()])
    comment = TextAreaField(label='Commentaire',validators=[Length(max=500)])
    date = DateField(label='Date de la candidature', validators=[
                     DataRequired()], format='%Y-%m-%d')
    date_last_relance = DateField('Date de relance', format='%Y-%m-%d')
    relance = BooleanField('A été relancé ? ')

    submit = SubmitField(label="Valider")


class ModifyProfile(FlaskForm):
    """[Form to modify profile]
    """
    last_name = StringField(label="Nom", validators=[DataRequired(), Length(max=50)])
    first_name = StringField(label="Prénom", validators=[DataRequired(), Length(max=50)])
    email_address = EmailField(label="Adresse mail:", validators=[DataRequired()])
    # street_number = StringField(label="Adresse mail:", validators = [DataRequired(), NumberRange(), Length(max=5)])
    telephone_number = StringField(label='Numéro de mobile :', validators=[Length(max=14)])
    file = FileField('file', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(label="Valider")



class CheckEmail(FlaskForm):
    """[Form to check the email]

    Args:
        FlaskForm ([type]): [description]
    """
    email = EmailField(label="Adresse mail:", validators=[DataRequired()])
    submit = SubmitField(label="Envoyer")
    
    
class CheckPwd(FlaskForm):
    """[Form to check the email]

    Args:
        FlaskForm ([type]): [description]
    """
    passw = PasswordField(validators=[DataRequired()])
    cpassw = PasswordField(validators=[DataRequired()])
    submit = SubmitField(label="Save")
    
    

class AddEvent(FlaskForm):
    """[form to add events to Calender
    """
    event_title = StringField(label='Event title', validators=[DataRequired()])
    start_date = DateField(label='Start Date', format='%Y-%m-%d')
    end_date = DateField(label='End Date', format='%Y-%m-%d')
    url = StringField(label='Url')
    submit = SubmitField(label="Valider")