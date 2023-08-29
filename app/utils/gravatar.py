# -*- encoding: utf-8 -*-
from typing import *
import hashlib
from urllib.parse import urlencode

import requests
import filetype


__all__ = ['GravatarFetcher', 'default_avatar', 'GravatarUpload']


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



class GravatarUpload:
    ALLOW_EXT = set(['jpg', 'jpeg', 'png', 'webp'])
    SAVE_DIR = '/avatar'

    def __init__(self, filename: str) -> None:
        self.__filename: str = filename
        self.__status: bool = self.validate_file(self.filename)

    def secure_filename(self):
        filename = self.filename.replace('//', '/').replace('\\', '/').rsplit('/', 1)[-1]
        ....

    def is_file_allowed(self) -> bool:
        if not (guess_result := filetype.guess(self.filename)):
            return False

        allow = GravatarUpload.ALLOW_EXT

        type_, spec = guess_result.mime.split('/')
        return guess_result.extension.lower() in allow and type_ == 'image' and spec.lower() in allow

    def validate_file(self) -> bool:
        return '.' in self.filename and self.is_file_allowed()

    @property
    def filename(self) -> str: return self.__filename

    @filename.setter
    def filename(self, filename: str) -> Optional[TypeError]:
        if not isinstance(filename, str):
            raise TypeError(f'Unsupported type {type(filename)} for `filename`')
        self.__filename = filename

    @classmethod
    def set_file(cls, filename) -> Self: return cls(filename)

    @property
    def status(self) -> bool: return self.__status
