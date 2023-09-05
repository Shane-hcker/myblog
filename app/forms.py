# -*- encoding: utf-8 -*-
import logging
from typing import *

from werkzeug.datastructures import FileStorage
from dns.resolver import NoResolverConfiguration

from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import (
    StringField, BooleanField, PasswordField, Field, 
    SubmitField, FileField, TextAreaField
)

from flask_wtf import FlaskForm, RecaptchaField

from .models import BlogUser
from .config import AppConfig

__all__ = ['UserLoginForm', 'UserRegForm', 'BasicForm']


class EmailValidator(Email):
    def __call__(self, *args, **kwargs):
        try:
            return super().__call__(*args, **kwargs)
        except NoResolverConfiguration:
            logging.warning('check_deliverability cannot operate properly, now set to False')
            self.check_deliverability = False
            return super().__call__(*args, **kwargs)


class UserForm(FlaskForm):
    email = StringField('Your Email:', validators=[DataRequired(),
                        EmailValidator('Invalid Email', check_deliverability=True)])
    username = StringField('Your Username:', validators=[DataRequired(), Length(min=4, max=32)])
    password = PasswordField('Your Password:', validators=[DataRequired(), Length(min=8)])
    # recaptcha = RecaptchaField()

    @property
    def general_uinfo(self) -> Dict[str, str]:
        return {
            'username': self.username.data,
            'email': self.email.data,
            'password': self.password.data
        }


class BasicForm(FlaskForm): 
    submit = SubmitField()


class UserLoginForm(UserForm):
    remember = BooleanField(label='Remember Me')
    login = SubmitField(label='Login')


class UserRegForm(UserForm):
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired()])
    register = SubmitField(label='Register')

    def validate_confirm_password(self, confirm_password: Field):
        if confirm_password.data != self.password.data:
            raise ValidationError('Passwords do not match.')

    def validate_username(self, username: Field):
        """
        validate_<field_name>
        """
        if BlogUser.get_uuser(username=username.data):
            raise ValidationError('Username already exists, please try again with other usernames')

    def validate_email(self, email: Field):
        if BlogUser.get_uuser(email=email.data):
            raise ValidationError('Email has been occupied or account already exists')


class ProfileEditForm(FlaskForm):
    avatar = FileField(label='Upload Your new avatar', name='avatar')
    username = StringField(label='Your Username', validators=[DataRequired(), Length(min=4, max=32)], 
                           name='username')
    email = StringField(label='Your Email: ', validators=[DataRequired(), Length(min=8),
                        EmailValidator('invalid email', check_deliverability=True)], name='email')
    # description = TextAreaField(label='Your Description: ')
    submit = SubmitField(label='Confirm Changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_avatar(self, avatar: Field):
        raw: FileStorage = avatar.raw_data[0]
        type_, ext = raw.content_type.split('/')
        if not (type_ == 'image' and ext in AppConfig.ALLOW_EXT):
            raise ValidationError(f'\'{raw.filename}\' uploaded is not a picture')

    def validate_username(self, username: Field):
        if self.original_username == username.data:
            return
        if BlogUser(False).filter_by(username=username).all():
            raise ValidationError('You need to have a unique username')

    def validate_email(self, email: Field):
        if self.original_email == email.data:
            return
        if BlogUser(False).filter_by(email=email).all():
            raise ValidationError('You need to have a unique email address')
