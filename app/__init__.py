# -*- encoding: utf-8 -*-
from typing import *
import flask
from flask_sqlalchemy import SQLAlchemy  # connector
from flask_migrate import Migrate  # db modification migrator

from app import config

app = flask.Flask(__name__)

# Load configuration
app.config.from_object(config.AppConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, datatypes
