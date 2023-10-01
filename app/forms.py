# -*- encoding: utf-8 -*-
from typing import *
from functools import wraps
import logging
import os
from dns.resolver import NoResolverConfiguration
from werkzeug.datastructures import FileStorage

from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms import (
    StringField, BooleanField, PasswordField, Field, 
    SubmitField, FileField, TextAreaField
)

from flask_wtf import FlaskForm, RecaptchaField

from .models import BlogUser
from .config import AppConfig

__all__ = ['UserLoginForm', 'UserRegForm', 'BasicForm', 'ProfileEditForm', 'SearchForm']


def check_character(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        field_data = args[-1].data
        for char in AppConfig.ILLEGAL_CHAR:
            if char in field_data:
                raise ValidationError(f'Containing illegal character: {", ".join(AppConfig.ILLEGAL_CHAR)}')
        return func(*args, **kwargs)
    return wrapper


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
    def userinfo(self) -> Dict[str, str]:
        return {
            'username': self.username.data,
            'email': self.email.data,
            'password': self.password.data
        }


class BasicForm(FlaskForm):
    submit = SubmitField()


class SearchForm(BasicForm):
    query = TextAreaField(label='搜索...')


class UserLoginForm(UserForm):
    username = email = None
    username_or_email = StringField('Your Username/Email...', validators=[DataRequired()])
    remember = BooleanField(label='Remember Me')
    login = SubmitField(label='Login')

    @check_character
    def validate_username(self, username: Field):
        pass

    @check_character
    def validate_email(self, email: Field):
        pass

    @check_character
    def validate_password(self, password: Field):
        pass


class UserRegForm(UserForm):
    confirm_password = PasswordField('Confirm your password', validators=[DataRequired()])
    register = SubmitField(label='Register')

    @check_character
    def validate_username(self, username: Field):
        """
        validate_<field_name>
        """
        if BlogUser.get_uuser(username=username.data):
            raise ValidationError('Username already exists, please try again with other usernames')

    @check_character
    def validate_email(self, email: Field):
        if BlogUser.get_uuser(email=email.data):
            raise ValidationError('Email has been occupied or account already exists')

    @check_character
    def validate_password(self, password: Field):
        pass

    def validate_confirm_password(self, confirm_password: Field):
        if confirm_password.data != self.password.data:
            raise ValidationError('Passwords do not match.')


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
        if not avatar.raw_data:
            return

        raw: FileStorage = avatar.raw_data[0]
        ext = os.path.splitext(raw.filename)[-1]
        if ext not in AppConfig.ALLOW_EXT:
            raise ValidationError(f'\'{raw.filename}\' uploaded is not a picture')

    @check_character
    def validate_username(self, username: Field):
        if self.original_username == username.data:
            return
        if BlogUser(False).filter_by(username=username).all():
            raise ValidationError('You need to have a unique username')

    @check_character
    def validate_email(self, email: Field):
        if self.original_email == email.data:
            return
        if BlogUser(False).filter_by(email=email).all():
            raise ValidationError('You need to have a unique email address')
