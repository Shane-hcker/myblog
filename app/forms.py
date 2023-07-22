# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.validators import (DataRequired, Length, Email, ValidationError)
from wtforms import (StringField, BooleanField, PasswordField,
    SubmitField, FileField, TextAreaField
)

from .models import BlogUser


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
    username = StringField(label='Your Username', validators=[DataRequired()])
    email = StringField(label='Your Email: ', validators=[DataRequired(),
                        Email('nvalid email', check_deliverability=True)])
    avatar = FileField(label='Upload Your new avatar')
    # description = TextAreaField(label='Your Description: ')
