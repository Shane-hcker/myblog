# -*- encoding: utf-8 -*-
from typing import *
import time
import flask
# Plugins
from flask_sqlalchemy import SQLAlchemy  # connector
from flask_migrate import Migrate  # db modification migrator
from flask_login import LoginManager  # user login manager

app = flask.Flask(__name__)

from app import config

# Load configuration
app.config.from_object(config.AppConfig)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # resembles url_for


current_time = lambda: time.strftime('%Y-%m-%d %H:%M')
success = lambda string: f'success;{string}'
fail = lambda string: f'fail;{string}'


def forEach(iterable: Iterable, func, ret_val=True) -> Optional[List[Any]]:
    res = [func(item) for item in iterable]
    if ret_val:
        return res


from app import routes, models, datatypes, errors
