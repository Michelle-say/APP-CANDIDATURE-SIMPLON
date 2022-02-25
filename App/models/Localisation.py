# from .. import db

# class Fonction(db.Model):
#     """Create a table fonction on to create a job like student, employee

#     Args:
#         db.Model: Generates columns for the table

#     """
#     id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
#     fonction = db.Column(db.String(), nullable=False)

#     def __repr__(self):
#         return f' Fonction : {self.fonction}'

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()