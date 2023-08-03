# -*- encoding: utf-8 -*-
from typing import *
from flask_mail import Message

from . import app, db, mail
from flask import render_template


def handle_error(func):
    def wrapper(*args, **kwargs):
        ...
    return wrapper


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error_500(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500
