# # allow to set variable is_active=True and to stay connected
# from flask_login import UserMixin
# from .. import db
# from Candidacy import Candidacy

# class Users(db.Model, UserMixin):
#     """Create a table Users on the candidature database

#     Args:
#         db.Model: Generates columns for the table
#         UserMixin: Generates an easy way to provide a current_user

#     """
#     id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
#     last_name = db.Column(db.String(length=30), nullable=False)
#     first_name = db.Column(db.String(length=30), nullable=False)
#     email_address = db.Column(db.String(length=50),nullable=False, unique=True)
#     password_hash = db.Column(db.String(length=200), nullable=False)
#     telephone_number = db.Column(db.String(length=10), nullable=True)
#     hashCode = db.Column(db.String(120))
#     is_admin = db.Column(db.Boolean(), nullable=False, default=False)
#     filename = db.Column(db.String(length=500))


#     def __repr__(self):
#         return f'{self.last_name} {self.first_name}'

#     def json(self):
#         return {
#             'last_name': self.last_name,
#             'first_name': self.first_name,
#             'email_address': self.email_address,
#             'telephone_number': self.telephone_number,
#             'is_admin': self.is_admin
#             }
    
#     def json_id(self):
#         return {
#             'id': self.id, 
#             'last_name': self.last_name, 
#             'first_name': self.first_name,
#             'email_address': self.email_address,
#             }


#     @classmethod
#     def find_by_title(cls, user_id):
#         return cls.query.filter_by(user_id=user_id).first()

#     @classmethod
#     def find_by_id(cls, id):
#         return cls.query.filter_by(id=id).first()

#     @classmethod
#     def find_all_isAdmin(cls):
#         return cls.query.filter_by(is_admin=True).all()

#     @classmethod
#     def find_all_isUsers(cls):
#         user_info=[]
#         for info in cls.query.filter_by(is_admin = False).all():
#             user_info.append(info.json_id())
#         return user_info

#     @classmethod
#     def find_by_user_id(cls, user_id):
#         user_info = []
#         for info in cls.query.filter_by(id=user_id).all():
#             user_info.append(info.json())
#         return user_info

#     @classmethod
#     def get_list_with_alternance(cls):
#         user_list = []
#         for user_info in cls.query.join(Candidacy).with_entities(Users.first_name, Users.last_name, Users.email_address, Candidacy.status, Candidacy.entreprise).all():

#             if user_info[3] == 'Alternance':
#                 user_list.append(user_info)

#         return user_list

#     @classmethod
#     def get_list_without_alternance(cls):

#         alternance_list = cls.query.join(Candidacy).with_entities(Users.id, Users.first_name,Users.last_name,Users.email_address,Candidacy.status, Candidacy.entreprise).all()

#         user_with_alternance_id=[]
#         unique_user_without_alternance_id = []
#         user_without_alternance=[]
#         all_user_list=[]

#         for info in cls.query.filter_by(is_admin = False).all():
#             all_user_list.append(info.json_id())

#         for user_info in alternance_list:
#             if user_info[4] == 'Alternance':
#                 user_with_alternance_id.append (user_info[0])

#         for user_info in all_user_list:
#             if (user_info['id'] not in user_with_alternance_id) and (user_info['id'] not in unique_user_without_alternance_id):
#                 user_without_alternance.append(user_info)
#                 unique_user_without_alternance_id.append (user_info['id']) 
   
#         return user_without_alternance

#     @classmethod
#     def get_full_list(cls):

#         full_list = cls.query.join(Candidacy).with_entities(
#             Users.id, Users.first_name, Users.last_name, Users.email_address, Candidacy.status, Candidacy.entreprise).all()
#         return full_list



#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()