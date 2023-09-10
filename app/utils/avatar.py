# -*- encoding: utf-8 -*-
import os.path
from typing import *

import flask
import requests
import pathlib

from PIL import Image


__all__ = ['Avatar']

from app import AppConfig


class Avatar:
    def __init__(self, fp):
        self.__img: Image = self.load_img(fp)
        self.src = fp if os.path.isfile(fp) else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(f'{exc_val}\n{exc_tb}')

    def save(self, file=None) -> Self:

        requests.post(flask.url_for('avatar', avatar=))

    def load_img(self, fp) -> Image:
        if isinstance(fp, (str, bytes, pathlib.Path)):
            return Image.open(fp)
        else:
            return Image.open(fp.read())

    def resize(self, size: int) -> Self:
        # todo reformat avatar.py + api, switch <img> to bg
        with Image.open(self.fp) as img:
            img.resize((size, size)).save()
        self.__img = self.img.resize((size, size))
        return self

    @staticmethod
    def default_avatar() -> str:
        return AppConfig.DEFAULT_AVATAR

    @property
    def img(self) -> Image: return self.__img
