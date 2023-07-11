# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

from app.utils.validators import ConfirmMatch


__all__ = ['UserLoginForm', 'UserRegForm']


class UserForm(FlaskForm):
    email = StringField(label='Your Email:', validators=[DataRequired(),
                        Email('Invalid Email', check_deliverability=True)])
    username = StringField(label='Your Username:', validators=[DataRequired(), Length(min=4, max=52)])
    password = PasswordField(label='Your Password:', validators=[DataRequired(), Length(min=8, max=64)])


class UserLoginForm(UserForm):
    remember = BooleanField(label='Remember Me!!!')
    login = SubmitField(label='Login')


class UserRegForm(UserForm):
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired(), ConfirmMatch()])
    remember = BooleanField(label='Remember Me!!!')
    register = SubmitField(label='Register')
