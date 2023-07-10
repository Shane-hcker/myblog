# -*- encoding: utf-8 -*-
from typing import *
from abc import ABCMeta, abstractmethod
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class UserForm(metaclass=BaseForm):
    email = StringField(label='Your Email:', validators=[DataRequired(),
                        Email('Invalid Email', check_deliverability=True)])
    username = StringField(label='Your Username:', validators=[DataRequired(), Length(min=4, max=52)])
    password = PasswordField(label='Your Password:', validators=[DataRequired(), Length(min=8, max=64)])

    @abstractmethod
    def foo(self): pass


class UserLoginForm(UserForm):
    remember = BooleanField(label='Remember Me!!!')
    login = SubmitField(label='Login')

    def foo(self): pass


class UserRegForm(UserLoginForm):
    confirm_password = StringField('Confirm your password', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me!!!')
    register = SubmitField(label='Register')

    def foo(self): pass
