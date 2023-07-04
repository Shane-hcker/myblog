# -*- encoding: utf-8 -*-
from typing import *
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class UserLoginForm(FlaskForm):
    email = StringField(label='Your Email:', validators=[DataRequired(),
                        Email('Invalid Email', check_deliverability=True)])
    username = StringField(label='Your Username:', validators=[DataRequired(), Length(min=4, max=52)])
    password = PasswordField(label='Your Password:', validators=[DataRequired(), Length(min=8, max=64)])
    remember = BooleanField(label='Remember Me next time when login')
    login = SubmitField(label='Login')
