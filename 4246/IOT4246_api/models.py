from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
import datetime

# db = SQLAlchemy()

class User(UserMixin): # db.Model):
    """
    Class to manage users.
    """

    # Function of class.
    def __init__(self, id, username, psw, is_admin = False):
        self.username = username
        self.psw = generate_password_hash(psw)
        self.is_admin = is_admin

        # TODO
        self.id = id
        # self.email = email

    def set_psw(self, psw):
        self.psw = generate_password_hash(psw)

    def check_psw(slef, psw):
        return check_psw_hash(self.psw, psw)

    def __repr__(self):
        return '<User {}>'.format(self.email)

# TODO:
# For debugging purposes.
# Create a list to save users logged in memory. 
# This list will delete if we reboot the server.
users = []

def get_user(username):
    """
    Search a user by 'username' into the list 'users'.
    """
    for user in users:
        if user.username == username:
            return user
    return None