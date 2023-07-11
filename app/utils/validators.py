# -*- encoding: utf-8 -*-
from typing import *
from wtforms.validators import (StopValidation, DataRequired)


__all__ = ['ConfirmMatch']


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
