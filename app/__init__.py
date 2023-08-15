# -*- encoding: utf-8 -*-
from typing import *
import time
import flask
import logging
from logging.handlers import SMTPHandler  # handling logging info
# Plugins
from flask_sqlalchemy import SQLAlchemy  # connector
from flask_migrate import Migrate  # db modification migrator
from flask_login import LoginManager  # user login manager
# from flask_mail import Mail  # send email
from flask_restful import Api

app = flask.Flask(__name__)
api = Api(app)

from app.config import AppConfig

# Load configuration
app.config.from_object(AppConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # resembles url_for

# Misc
current_time = lambda: time.strftime('%Y-%m-%d %H:%M')
success = lambda string: f'success;{string}'
fail = lambda string: f'fail;{string}'


@lambda _: _()
def add_handler_immediate() -> None:
    '''Testing Handler:
    >>> python -m smtpd -n -c DebuggingServer localhost:...
    >>> export FLASK_ENV=production
    >>> export MAIL_HOST=...
    >>> export MAIL_PORT=...
    '''
    if app.debug:
        return
    if not (host := app.config.get('MAIL_HOST')):
        return

    username, pwd = app.config.get('MAIL_USERNAME'), app.config.get('MAIL_PASSWORD')
    cred: Tuple[str, str] = (username, pwd) if username or pwd else None
    secure = () if app.config.get('MAIL_USE_SSL') else None

    mail_handler = SMTPHandler(
        mailhost=(host, app.config.get('MAIL_PORT')),
        fromaddr=username,
        toaddrs=app.config.get('ADMINS'),
        subject=f'Blog Failure {time.strftime("%Y:%m:%d %H:%M:%S")}',
        credentials=cred, secure=secure
    )
    mail_handler.setLevel(logging.ERROR)  # only reports error msgs
    app.logger.addHandler(mail_handler)


from app import routes, apis, errors, models, datatypes
