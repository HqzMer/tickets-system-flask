from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,PasswordField
from wtforms.validators import DataRequired

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
