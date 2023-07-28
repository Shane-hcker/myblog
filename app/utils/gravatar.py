# -*- encoding: utf-8 -*-
from typing import *
import requests
import hashlib
from urllib.parse import urlencode


__all__ = ['GravatarFetcher']


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

    def fetch(self, size=10) -> Self:
        query = {'s': size}
        query.update({'d': self.default}) if self.default else ...
        hashed = self.__hash_email(self.email)
        self.url = GravatarURL(f'{self.__class__.URL}{hashed}/?{urlencode(query)}')
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
