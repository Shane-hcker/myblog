# -*- encoding: utf-8 -*-
from typing import *
from io import BufferedReader
import pathlib

from PIL import Image


__all__ = ['Avatar']

from app import AppConfig


class Avatar:
    def __init__(self, fp):
        self.__img: Image = self.load_img(fp)
        self.src = fp if isinstance(fp, (str, pathlib.Path)) else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(f'{exc_val}\n{exc_tb}')

    def save(self, file=None) -> Self:
        if not (file or self.src):
            raise TypeError(f'Either`file` or `{self}.src` should not be None')
        self.src = file or self.src
        self.__img.save(self.src)
        return self

    def load_img(self, fp) -> Image:
        if isinstance(fp, (str, bytes, pathlib.Path)):
            return Image.open(fp)
        else:
            return Image.open(fp.read())

    def resize(self, size: int) -> Self:
        self.__img = self.__img.resize((size, size))
        return self

    @staticmethod
    def default_avatar() -> str:
        return AppConfig.DEFAULT_AVATAR.rsplit('/', 1)[-1]

    @property
    def img(self) -> Image: return self.__img
