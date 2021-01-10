from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, DateField, IntegerField, RadioField, BooleanField, FileField, \
    PasswordField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Regexp


class SignInForm(FlaskForm):
    username = StringField('Username:',
                       validators=[DataRequired("Name can't be null")],
                        render_kw={'placeholder': 'Your username'})
    email = StringField('Email address:',
                        validators=[DataRequired("Email can't be null")],
                        render_kw={'placeholder': 'Your email'})
    password = PasswordField('Password:',
                        validators=[DataRequired("Password can't be null")],
                        render_kw={'placeholder': 'Enter password'})
    passwordConfirm = PasswordField('Password Confirm:',
                        validators=[DataRequired("Password confirm can't be null")],
                        render_kw={'placeholder': 'Enter password again'})
    submit = SubmitField('Sign in')


class LoginForm(FlaskForm):
    email = StringField('Email address:',
                        validators=[DataRequired("Email can't be null")],
                        render_kw={'placeholder': 'Your email'})
    password = PasswordField('Password:',
                        validators=[DataRequired("Password can't be null")],
                        render_kw={'placeholder': 'Enter password'})
    submit = SubmitField('Sign in')


class AddCommentForm(FlaskForm):
    content = TextAreaField('Looking forward to hearing you',
                          validators=[DataRequired("Content can't be null")],
                          render_kw={'placeholder': 'Enter your comment here',
                                     'style': 'width:100%; '
                                              'height:200px; '
                                              'margin-top:20px;'
                                              'font-size: large;'
                                              'background-color:#757575;'
                                              'border-style: double;'
                                              'margin-left:30px;'
                                              'resize:none'})
    submit = SubmitField('Submit',
                         render_kw={'style': 'width:100%;'
                                             'margin-left:30px;'
                                             'height:100%;'
                                             'margin-top:10px;'
                                             'font-size: large;'
                                             'background-color:#757575;'})


class PersonalEditForm(FlaskForm):
    nickname = StringField('Nickname:',
                           validators=[DataRequired('Have a nickname sounds great too!')],
                           render_kw={'placeholder': 'Enter your special name'})
    fullname = StringField('Fullname:',
                           validators=[DataRequired('Enter your full name here')],
                           render_kw={'placeholder': 'Enter your full name'})
    birthday = StringField('Birthday', validators=[DataRequired()],
                           render_kw={'placeholder': 'YYYY-MM-DD'})
    presentation = TextAreaField('Personal Introduction:',
                                 validators=[DataRequired()],
                                 render_kw={'style': 'width:100%;'
                                                     'height:100px;'
                                                     'resize:none',
                                            'placeholder': 'Share you with friends'})
    gender = RadioField('Gender',
                        validators=[DataRequired("Please choose your gender")],
                        choices=['Male', 'Female'])
    avatar = FileField('Your Avatar', validators=[FileRequired(), FileAllowed(['jpg'], 'Only jpg files please')])
    country = SelectField('Country', validators=[DataRequired()],
                          choices=['China', 'America', 'Canada', 'India', 'Russia', 'Ireland', 'England', 'France', 'Germany'],
                          default='China')
    submit = SubmitField('Submit',
                         render_kw={'style': 'width:80%;'
                                             'height:50%;'
                                             'margin-Top:70px;'
                                             'margin-Left:80px;'
                                             'background-Color:gray'})


class AlgorithmEditForm(FlaskForm):
    name = StringField('Algorithm Name:',
                       validators=[DataRequired()],
                       render_kw={'style': 'width:80%;'
                                           'height:50px'})
    code_pic = FileField('Add your code picture here',
                         validators=[FileRequired(), FileAllowed(['jpg'], 'Only jpg files please')])
    theory = TextAreaField('Explain your algorithm:',
                         validators=[DataRequired()],
                         render_kw={'style': 'width:80%;'
                                             'height:50px'})
    complexity = TextAreaField('Complexity:',
                             validators=[DataRequired()],
                             render_kw={'style': 'width:80%;'
                                                 'height:50px'})
    application = TextAreaField('How can this algorithm has been use:',
                              validators=[DataRequired()],
                              render_kw={'style': 'width:80%;'
                                                  'height:50px'})
    submit = SubmitField('Submit',
                         render_kw={'style': 'width:40%;'
                                             'height:50%;'
                                             'margin-Top:40px;'
                                             'margin-Left:80px;'
                                             'background-Color:gray'})
