# -*- encoding: utf-8 -*-
from typing import *
import os
import hashlib
from urllib.parse import urlencode

from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
import requests


__all__ = ['Gravatar', 'default_avatar']


class Gravatar:
    URL = 'https://www.gravatar.com/avatar/'

    def __init__(self, email: str, default='mp') -> None:
        self.email = email.strip() if email else ''
        self.default = default
        self.url = None

    def __str__(self) -> str:
        return self.url

    def fetch(self, size=50) -> Self:
        query = {'s': size or 50}
        query.update({'d': self.default}) if self.default else ...
        hashed = self.__hash_email(self.email)
        self.url = GravatarURL(f'{self.URL}{hashed}/?{urlencode(query)}')
        return self

    def save(self, filename) -> None:
        self.url.save(filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(exc_val)

    @staticmethod
    def __hash_email(email):
        if not email:
            raise ValueError(f'parameter \'email\' should be not None')
        return hashlib.md5(email.lower().encode()).hexdigest()

    __repr__ = __str__


class GravatarURL(str):
    def save(self, filename) -> None:
        with open(filename, 'wb') as f:
            f.write(requests.get(self.url).content)


def default_avatar(email, size=100) -> str:
    with Gravatar(email) as fetcher:
        return fetcher.fetch(size).url
