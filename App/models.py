import datetime
# allow to set variable is_active=True and to stay connected
from flask_login import UserMixin
import logging as lg
from werkzeug.security import generate_password_hash
import csv
import difflib as dif
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    """Allow to create a current_user with his id
    Args:
        user_id (int): user_id from the database
    Returns:
        instance of users depending of his id
    """
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    """Create a table Users on the candidature database

    Args:
        db.Model: Generates columns for the table
        UserMixin: Generates an easy way to provide a current_user

    """
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    last_name = db.Column(db.String(length=30), nullable=False)
    first_name = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=200), nullable=False)
    telephone_number = db.Column(db.String(length=10), nullable=True)
    hashCode = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    filename = db.Column(db.String(length=500))


    def __repr__(self):
        return f'{self.last_name} {self.first_name}'

    def json(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'email_address': self.email_address,
            'telephone_number': self.telephone_number,
            'is_admin': self.is_admin
            }
    
    def json_id(self):
        return {
            'id': self.id, 
            'last_name': self.last_name, 
            'first_name': self.first_name,
            'email_address': self.email_address,
            }


    @classmethod
    def find_by_title(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all_isAdmin(cls):
        return cls.query.filter_by(is_admin=True).all()

    @classmethod
    def find_all_isUsers(cls):
        user_info=[]
        for info in cls.query.filter_by(is_admin = False).all():
            user_info.append(info.json_id())
        return user_info

    @classmethod
    def find_by_user_id(cls, user_id):
        user_info = []
        for info in cls.query.filter_by(id=user_id).all():
            user_info.append(info.json())
        return user_info

    @classmethod
    def get_list_with_alternance(cls):
        user_list = []
        for user_info in cls.query.join(Candidacy).with_entities(Users.first_name, Users.last_name, Users.email_address, Candidacy.status, Candidacy.entreprise).all():

            if user_info[3] == 'Alternance':
                user_list.append(user_info)

        return user_list

    @classmethod
    def get_list_without_alternance(cls):

        alternance_list = cls.query.join(Candidacy).with_entities(Users.id, Users.first_name,Users.last_name,Users.email_address,Candidacy.status, Candidacy.entreprise).all()

        user_with_alternance_id=[]
        unique_user_without_alternance_id = []
        user_without_alternance=[]
        all_user_list=[]

        for info in cls.query.filter_by(is_admin = False).all():
            all_user_list.append(info.json_id())

        for user_info in alternance_list:
            if user_info[4] == 'Alternance':
                user_with_alternance_id.append (user_info[0])

        for user_info in all_user_list:
            if (user_info['id'] not in user_with_alternance_id) and (user_info['id'] not in unique_user_without_alternance_id):
                user_without_alternance.append(user_info)
                unique_user_without_alternance_id.append (user_info['id']) 
   
        return user_without_alternance

    @classmethod
    def get_full_list(cls):

        full_list = cls.query.join(Candidacy).with_entities(
            Users.id, Users.first_name, Users.last_name, Users.email_address, Candidacy.status, Candidacy.entreprise).all()
        return full_list



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Candidacy(db.Model):
    """Create a table Candidacy on the candidature database

    Args:
        db.Model: Generates columns for the table

    """

    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),nullable=False)
    entreprise = db.Column(db.String(), nullable=True)
    ville_entreprise = db.Column(db.String(), nullable=True)
    contact_full_name = db.Column(db.String(length=50), nullable=False)
    contact_email = db.Column(db.String(length=50), nullable=True)
    contact_mobilephone = db.Column(db.String(length=50), nullable=True)
    date = db.Column(db.String(), nullable=True, default= datetime.date.today())
    status = db.Column(db.String(), nullable=True, default="En cours")
    comment = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f' Candidat id : {self.user_id}'

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'entreprise': self.entreprise,
            'ville_entreprise': self.ville_entreprise,
            'contact_full_name': self.contact_full_name,
            'contact_email': self.contact_email,
            'contact_mobilephone': self.contact_mobilephone,
            'date': self.date,
            'status': self.status,
            'comment': self.comment
        }

    def json_test(self):
        return {

            'entreprise': self.entreprise,
            'contact_full_name': self.contact_full_name,
            'contact_email': self.contact_email,
            'status': self.status
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        candidacy_list = []
        for candidacy in cls.query.filter_by(user_id=user_id).all():
            candidacy_list.append(candidacy.json())
        return candidacy_list
    
    @classmethod
    def check_entreprise_exist(cls,entreprise):
        entreprise_commune = []
        for candidacy in cls.query.group_by(cls.entreprise).with_entities(cls.entreprise):
            ratio = dif.SequenceMatcher(a=candidacy.entreprise, b=entreprise).ratio()
            if ratio > 0.75 and ratio < 1:
                entreprise_commune.append('- ' + candidacy.entreprise)
        return entreprise_commune
        

    @classmethod
    def get_all_in_list_with_user_name(cls):
        candidacy_list = []
        for candidacy in cls.query.join(Users).with_entities(Users.first_name, cls.id, cls.entreprise, cls.contact_full_name, cls.contact_email, cls.contact_mobilephone, cls.date, cls.status).all():
            candidacy_list.append(candidacy)
        return candidacy_list

    @classmethod
    def get_all_in_list_entreprise(cls):
        entreprise_list=[]
        # for entreprise_info in cls.query.join(Users).with_entities(Users.first_name, Users.last_name, cls.user_id ,cls.entreprise,cls.entreprise_ville, cls.contact_full_name, cls.contact_email, cls.contact_mobilephone).all():
        for entreprise_info in cls.query.join(Users).with_entities(cls.user_id ,cls.entreprise,cls.ville_entreprise, cls.contact_full_name, cls.contact_email, cls.contact_mobilephone).all():
            entreprise_list.append(entreprise_info)
        return entreprise_list

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Fonction(db.Model):
    """Create a table fonction on to create a job like student, employee

    Args:
        db.Model: Generates columns for the table

    """
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    fonction = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f' Fonction : {self.fonction}'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# Function to create db and populate it
def init_db():
    db.drop_all()
    db.create_all()
    #db.session.add( )

    Users(last_name="ben", first_name="charles", email_address="cb@gmail.com",
          password_hash=generate_password_hash("1234", method='sha256'), is_admin=True).save_to_db()
    Users(last_name="beniac", first_name="cha", email_address="bb@gmail.com",
          password_hash=generate_password_hash("1234", method='sha256'), is_admin=False).save_to_db()
    #Candidacy(user_id = 1, entreprise = "facebook", contact_full_name = "mz", contact_email="mz@facebook.fb").save_to_db()
    #Candidacy(user_id = 1, entreprise = "google", contact_full_name = "lp", contact_email="lp@gmail.com").save_to_db()

    lg.warning('Ouverture du fichier CSV liste_apprenants')

    # Insert all users from  "static/liste_apprenants.csv"
    with open("App/static/liste_apprenants.csv", newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
   
    for i in data:
        user = {
            'email_address': i[0],
            'first_name': i[1],
            'last_name': i[2],
            'password_hash': generate_password_hash(i[3], method='sha256'),
            'is_admin': True if i[4] == "TRUE" else False
        }
        Users(**user).save_to_db()

    lg.warning('Ouverture du fichier CSV Candidacy')
    with open("App/static/candidacy.csv", newline='') as fileCandi:
        readerCandi = csv.reader(fileCandi)
        dataCandi = list(readerCandi)

    lg.warning('Debut enregistrement Candidacy')
    for i in dataCandi:
        candidacy = {
            'user_id': i[0],
            'entreprise': i[1],
            'contact_full_name': i[2],
            'contact_email': i[3],
            'contact_mobilephone': i[4],
            'date': i[5],
            'status': i[6]
        }
        Candidacy(**candidacy).save_to_db()

    lg.warning('Ouverture du fichier CSV fonction')
    with open("App/static/fonction.csv", newline='') as filefonction:
        reader = csv.reader(filefonction)
        data = list(reader)
        print(data)

    lg.warning('Debut enregistrement fonction')
    for i in data:
        Fonction(fonction=i[0]).save_to_db()

    lg.warning('Database initialized!')
