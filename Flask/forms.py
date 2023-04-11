from wtforms import Form, StringField, TextField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.fields import BooleanField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(Form):
    """
    Class to manage logins.
    """

    # Variables.
    email = StringField('Email', validators = [DataRequired()])
    psw = PasswordField('psw', validators = [DataRequired()])

    # Rember session.
    remember_login = BooleanField('Remember')

    # Login action.
    submit = SubmitField('Login')