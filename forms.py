from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,IntegerField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo,required


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),Length(max=50)])
    surname = StringField('Surname',
                       validators=[DataRequired(),Length(max=50)])

    gender = SelectField('gender', choices=[('Male','Male'), ('Female','Female')], default=2, validators=[DataRequired()])

    age = StringField('Age',
                       validators=[DataRequired(),required(),Length(min=1, max=3)])

    email = StringField('Email',
                        validators=[DataRequired(), Email(),Length(max=50)])

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

class editPublisher(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),Length(max=40)])
    address = StringField('Address',
                            validators=[DataRequired()])

    date = DateField('Establishment Date',
                          validators=[DataRequired(),required()])

    companyName = StringField('Comp. Name',
                          validators=[DataRequired(),Length(max=50)])

    numOfBooks = IntegerField('Num of Books',
                         validators=[DataRequired()])

    submit = SubmitField('submit')

class editAuthor(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(),Length(max=30)])
    surname = StringField('Surname',
                            validators=[DataRequired()])

    date = DateField('Date',
                          validators=[DataRequired(),required()])

    country = StringField('Country',
                          validators=[DataRequired(),Length(max=40)])

    numOfBooks = IntegerField('Num of books',
                         validators=[DataRequired(),required()])

    submit = SubmitField('submit')