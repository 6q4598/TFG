import sqlite3
import json
import forms
import models
from flask import Flask, render_template, request, make_response, session, flash, g, url_for, redirect, jsonify
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
# from models import *
# from flask_wtf import CsrfProtect

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

    # if 'username' in session:
    #     print("USER REGISTERED MADAFAKAS")
    # else:
    #     print("PROBLEM HAS OCURRED NONON DJKLDAJLDFÑKAJDFLKÑAJÑ -------------------------------------------------------------------------------")

    # TODO
    ##############################
    valuesOee = [32, 14, 43, 11]
    valuesOkNok = [3200, 1400]
    valuesMachines = [80, 15, 25, 20]
    values4char = [((0.96 * 0.90 * 0.94) * 100), 90, 96, 94]
    ##############################

    return render_template("index.html", valuesOee = valuesOee, valuesOkNok = valuesOkNok, valuesMachines = valuesMachines, values4char = values4char)
    # , form = login_form)


# LOGIN
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

# LOGOUT
@app.route('/logout', methods = ['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return(redirect(url_for('index')))

    """
    Values for pieces chart.
    """
    models.get_pieces()
    return jsonify(sensor1=valor_sensor1, sensor2=valor_sensor2)

@app.route('/pieces')
def pieces():
    """
    Database query to get the pieces fabricated (OK and NOK).
    """
    result = models.Plc().get_pieces()
    return jsonify(pieces_ok = result[0], pieces_nok = result[1])

@app.route('/oee')
def oee():
    """
    Database query to get the pieces fabricated (OK and NOK).
    """
    result = models.Plc().get_oee()
    return jsonify(availability = result[0], performance = result[1], quality = result[2])

if __name__=='__main__':
    app.run()
