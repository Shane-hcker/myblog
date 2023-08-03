# -*- encoding: utf-8 -*-
from functools import wraps, partial
import logging

import flask

from app.models import BlogUser


__all__ = ['error_log', 'check_valid_username']


def error_log(func=None, *, level=logging.warning, error_callback=lambda: None):
    if not func:
        return partial(error_log, level=level, error_callback=error_callback)

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            level(msg=e)
            return error_callback()
    return inner


def check_valid_username(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = kwargs['username']
        name_list = [user['username'] for user in BlogUser.fetch_all_users('username')]
        if username in name_list:
            return func(*args, **kwargs)
        return flask.redirect('errors/404.html')
    return wrapper
