# -*- encoding: utf-8 -*-
import logging
from typing import *

from dns.resolver import NoResolverConfiguration

from flask_wtf import FlaskForm, RecaptchaField
from wtforms.validators import (DataRequired, Length, Email, ValidationError)
from wtforms import (StringField, BooleanField, PasswordField,
                     SubmitField, FileField, TextAreaField)

from .models import BlogUser


__all__ = ['UserLoginForm', 'UserRegForm']


class EmailValidator(Email):
    def __call__(self, *args, **kwargs):
        try:
            return super().__call__(*args, **kwargs)
        except NoResolverConfiguration:
            logging.warning('check_deliverability can operate properly, now set to False')
            self.check_deliverability = False
            return super().__call__(*args, **kwargs)


class UserForm(FlaskForm):
    email = StringField('Your Email:', validators=[DataRequired(),
                        EmailValidator('Invalid Email', check_deliverability=True)])
    username = StringField('Your Username:', validators=[DataRequired(), Length(min=4, max=52)])
    password = PasswordField('Your Password:', validators=[DataRequired(), Length(min=8)])
    # recaptcha = RecaptchaField()

    @property
    def general_uinfo(self) -> Dict[str, str]:
        return {
            'username': self.username.data,
            'email': self.email.data,
            'password': self.password.data
        }


class UserLoginForm(UserForm):
    remember = BooleanField(label='Remember Me!!!')
    login = SubmitField(label='Login')


class UserRegForm(UserForm):
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired()])
    register = SubmitField(label='Register')

    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.password.data:
            raise ValidationError('Passwords do not match.')

    def validate_username(self, username):
        """
        validate_<field_name>
        """
        if BlogUser.get_uuser(username=username.data):
            raise ValidationError('Username already exists, please try again with other usernames')

    def validate_email(self, email):
        if BlogUser.get_uuser(email=email.data):
            raise ValidationError('Email has been occupied or account already exists')


class ProfileEditForm(FlaskForm):
    avatar = FileField(label='Upload Your new avatar')
    username = StringField(label='Your Username', validators=[DataRequired(), Length(min=4, max=52)])
    email = StringField(label='Your Email: ', validators=[DataRequired(), Length(min=8),
                        EmailValidator('invalid email', check_deliverability=True)])
    # description = TextAreaField(label='Your Description: ')
    submit = SubmitField(label='Confirm Changes')
