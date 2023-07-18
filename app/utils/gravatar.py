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

    def __init__(self, email: str, default=None) -> None:
        self.email = email.strip()
        self.default = default if default else 'mp'

    def fetch(self, size=10) -> GravatarURL:
        query = {'s': size}
        query.update({'d': self.default}) if self.default else ...
        hashed = self.__hash_email()
        return GravatarURL(f'{self.__class__.URL}{hashed}/?{urlencode(query)}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __hash_email(self, email=None):
        if not email and not self.email:
            raise ValueError(f'Either `email` or `{self}.email` should be not None')
        return hashlib.md5((email or self.email).lower().encode()).hexdigest()
