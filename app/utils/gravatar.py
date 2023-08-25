# -*- encoding: utf-8 -*-
from typing import *
import hashlib
from urllib.parse import urlencode

import requests
import filetype


__all__ = ['GravatarFetcher', 'default_avatar']


def default_avatar(email, size=100) -> str:
    with GravatarFetcher(email) as fetcher:
        return fetcher.fetch(size).url


class GravatarURL(str):
    def save(self, filename=None) -> None:
        with open(filename, 'wb') as f:
            f.write(requests.get(self).content)


class GravatarFetcher:
    URL = 'https://www.gravatar.com/avatar/'

    def __init__(self, email: str, default='mp') -> None:
        self.email = email.strip()
        self.default = default
        self.url = None

    def __str__(self) -> str:
        return self.url

    def fetch(self, size=None) -> Self:
        query = {'s': size or 50}
        query.update({'d': self.default}) if self.default else ...
        hashed = self.__hash_email(self.email)
        self.url = GravatarURL(f'{self.URL}{hashed}/?{urlencode(query)}')
        return self

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



class GravatarUploader:
    ALLOW_EXT = set(['jpg', 'jpeg', 'png', 'webp'])

    @staticmethod
    def validate_file(filename) -> bool:
        return '.' in filename and GravatarUploader.is_file_allowed(filename)

    @staticmethod
    def is_file_allowed(filename) -> bool:
        guess = filetype.guess(filename)
        if not guess:
            return False

        allow = GravatarUploader.ALLOW_EXT

        type_, spec = guess.mime.split('/')
        return guess.extension in allow and type_ == 'image' and spec in allow
