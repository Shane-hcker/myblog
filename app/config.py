# -*- encoding: utf-8 -*-
from typing import *
import os
from random import randint
from sqlalchemy import URL


__all__ = ['AppConfig']


def genKey() -> str:
    return ''.join([chr(randint(48, 122)) for _ in range(32)])


class AppConfig:
    # env secret key or hard-coded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or genKey()

    # RECAPTCHA_PUBLIC_KEY
    # RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = URL.create('mysql+pymysql', host='localhost', port=3306,
                                         username='root', database='learn_mysql',  password='12345678')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
