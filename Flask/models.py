import datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

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

class Plc():
    """
    Class to comunications with database.
    """

    def __init(self):
        return

    def get_pieces(self):
        """
        Get pieces OK and NOK from database.
        """
        result = []
        sql_query = "SELECT SUM(OK), SUM(NOK) FROM table_plc WHERE date = '{}'".format(
            # time.strftime("03/21/23"))
            "03/21/23")

        print(sql_query)
        conn = sqlite3.connect('static/BD/4246_IOT.db')
        c = conn.cursor()
        c.execute(sql_query)
        rows = c.fetchmany()
        result.append(rows[0][0])
        result.append(rows[0][1])
        return result

    def get_oee(self):
        """
        Get current Availability, Performance and Quality from table_oee.
        """
        result = []
        sql_query = "SELECT Availability, Performance, Quality FROM table_oee WHERE Date = '{}' ORDER BY Hour DESC LIMIT 1".format(
            # time.strftime("%D")
            "03/21/23")

        print(sql_query)
        conn = sqlite3.connect('static/BD/4246_IOT.db')
        c = conn.cursor()
        c.execute(sql_query)
        rows = c.fetchmany()
        result.append(rows[0][0])
        result.append(rows[0][1])
        result.append(rows[0][2])
        return result

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
