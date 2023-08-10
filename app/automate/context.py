# -*- encoding: utf-8 -*-
from typing import *
from app import app


def __del__(self):
    self.app_context.pop()


def app_context(cls) -> object:
    cls.app_context = app.app_context()
    cls.app_context.push()
    cls.__del__ = __del__
    return cls
