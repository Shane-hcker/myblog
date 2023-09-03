# -*- encoding: utf-8 -*-
from typing import *
import os
from random import randint
from sqlalchemy import URL


__all__ = ['AppConfig']


def gen_key() -> str:
    return ''.join([chr(randint(48, 122)) for _ in range(32)])


def content_length(size: str):
    size, suffix = int(size[:-2]), size[-2:].upper()
    match suffix:
        case 'B':
            return size
        case 'KB':
            return size * 1024
        case 'MB':
            return size * (1024 ** 2)
        case _:
            raise MemoryError('Memory exceeded.')


class AppConfig:
    # env secret key or hard-coded string
    SECRET_KEY = os.environ.get('SECRET_KEY') or gen_key()

    # RECAPTCHA_PUBLIC_KEY
    # RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # Filing
    MAX_CONTENT_LENGTH = content_length('32MB')
    ALLOW_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    AVATAR_SAVE_DIR = 'static/avatar/'

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = URL.create('mysql+pymysql', host='localhost', port=3306,
                                         username='root', database='learn_mysql',  password='12345678')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mailing Config
    MAIL_HOST = os.environ.get('MAIL_HOST')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['shanebilibili@outlook.com', 'shanexiangxbw@gmail.com']
