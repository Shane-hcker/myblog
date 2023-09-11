# -*- encoding: utf-8 -*-
import os
from typing import *
from PIL import Image
import flask
import requests
import pathlib

from app import AppConfig


__all__ = ['Avatar']


class Avatar:
    def __init__(self, *, raw=None, imgpath=None) -> None:
        self.raw = raw
        self.imgpath = imgpath

    def save(self, imgpath: str, mod_path=False) -> Self:
        with open(imgpath, 'wb') as f:
            f.write(self.raw or self.raw_from_path(self.imgpath))
        if mod_path:
            self.imgpath = imgpath
        return self

    @staticmethod
    def default_avatar():
        return '/default.png'

    @staticmethod
    def raw_from_path(imgpath) -> bytes:
        with open(imgpath, 'rb') as f:
            return f.read()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(f'{exc_val} at {exc_tb}')

