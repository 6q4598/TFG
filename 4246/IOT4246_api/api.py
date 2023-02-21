from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():

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

if __name__=='__main__':

    app.run()