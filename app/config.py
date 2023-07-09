# -*- encoding: utf-8 -*-
from typing import *
import os
from random import randint
from sqlalchemy import URL


__all__ = ['AppConfig']


class AppConfig:
    # env secret key or hard-coded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''.join([chr(randint(48, 122)) for i in range(32)])
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = URL.create('mysql+pymysql', host='localhost', port=3306,
                                         username='root', database='learn_mysql',  password='12345678')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
