from flask import Flask, render_template, request, make_response, session, flash, g, url_for, redirect
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
# from flask_wtf import CsrfProtect
from werkzeug.urls import url_parse
import sqlite3
import json

import forms
import models

from models import *

app = Flask(__name__)

# CSRF protect.
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

# Flask login.
login = LoginManager(app)
login.login_vie = "login"

###################################
valuesOee = []
valuesMachines = []
values4char = []
###################################

# A 'middleware' that executes before to response to any request.
@app.before_request
def verify_login_before():
    """
    Verify that the user is logged in.
    """
    route = request.path
    if 'username' in session:
        print("USERNAME IS LOGGED")
    else:
        print("NOT LOGGED USERNAME")
    # return '0' if 'username' in session else '1'.

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET'])
def index():

    # TODO TODO TODO TODO
    # if 'username' in session:
    #     print("USER REGISTERED MADAFAKAS")
    # else:
    #     print("PROBLEM HAS OCURRED NONON DJKLDAJLDFÑKAJDFLKÑAJÑ -------------------------------------------------------------------------------")
    # TODO TODO TODO TODO

    # DB values for represent the charts with Chart.js.
    #############################################################################
    valuesOkNok = []
    conn = sqlite3.connect('static/BD/esp32.db')
    c = conn.cursor()
    c.execute("SELECT SUM(OK), SUM(NOK) FROM esp32_table");

    rows = c.fetchmany()
    valuesOkNok.append(rows[0][0])
    valuesOkNok.append(rows[0][1])

    # TODO
    ##############################
    valuesOee = [32, 14, 43, 11]
    valuesMachines = [80, 15, 25, 20]
    values4char = [((0.96 * 0.90 * 0.94) * 100), 90, 96, 94]
    ##############################

    return render_template("index.html", valuesOee = valuesOee, valuesOkNok = valuesOkNok, valuesMachines = valuesMachines, values4char = values4char)
    # , form = login_form)


###################################################
# LOGIN                                           #
###################################################
@app.route('/login', methods=['POST'])
@login.user_loader
def login():
    """
    Login view.
    -----------
    Tests:
    .......
    """
    username = request.form.get("user")
    psw = request.form.get("psw")
    session['username'] = username
    print("User '" + username + "' has been logged correctly.")
    return(redirect(url_for('index')))

###################################################
# LOGOUT                                          #
###################################################
@app.route('/logout', methods = ['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return(redirect(url_for('index')))

if __name__=='__main__':
    app.run()
