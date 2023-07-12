# -*- encoding: utf-8 -*-
from typing import *
from functools import wraps
import flask

# Plugins
from flask_login import current_user
from wtforms.validators import (StopValidation)


__all__ = ['ConfirmMatch', 'loginRequired']


class ConfirmMatch:
    def __init__(self, message=None) -> None:
        self.message = message
        self.field_flags = {'required': True}

    def __call__(self, form, field):
        if form.password.data == field.data:
            return

        if self.message is None:
            message = field.gettext("Passwords do not match")
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)


def loginRequired(redirection, flash_message=None):
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal flash_message
            if not flash_message:
                flash_message = 'please login to access this page'

            if not current_user.is_authenticated:
                flask.flash(flash_message)
                return flask.redirect(flask.url_for(redirection))

            return func(*args, **kwargs)
        return inner
    return outer
