from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired()])
    surname = StringField('Surname',
                       validators=[DataRequired()])

    gender = SelectField('gender', choices=[('Male','Male'), ('Female','Female')], default=2, validators=[DataRequired()])

    age = StringField('Age',
                       validators=[DataRequired(),Length(min=1, max=3)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=6,max=9)])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])


    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AddUserContent(FlaskForm):
    book = StringField('FavBook',
                       validators=[DataRequired()])
    publisher = StringField('FavPublisher',
                       validators=[DataRequired()])

    author = StringField('Favauthor',
                        validators=[DataRequired()])

    submit = SubmitField('submit')