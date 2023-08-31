# -*- encoding: utf-8 -*-
from typing import *
import os
import hashlib
from urllib.parse import urlencode

from flask import request
from werkzeug.datastructures.file_storage import FileStorage
import requests
import filetype


__all__ = ['GravatarFetcher', 'default_avatar', 'Avatar']


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


class GravatarGenerator:
    pass


class Avatar:
    """
    >>> avatar = Avatar(avatar)
    >>> avatar.is_valid
    """
    ALLOW_EXT = set(['jpg', 'jpeg', 'png', 'webp'])
    SAVE_DIR = '/avatar'

    def __init__(self, file: FileStorage) -> None:
        self.__file: FileStorage = file
        self.__valid: bool = self.__validate_file(self.file)

    def __validate_file(self, file: FileStorage) -> bool:
        if not isinstance(file, FileStorage):
            raise TypeError('Attribute `file` should only be type `FileStorage`')

        return '.' in file.filename and self.__is_file_allowed(self.file)

    def __is_file_allowed(self, file: FileStorage) -> bool:
        if (guess_result := filetype.guess(file.filename)):
            return False

        return guess_result.mime.split('/')[-1].lower() in self.ALLOW_EXT

    def save(self) -> None:
        self.file.save(os.path.join(self.SAVE_DIR, self.secure_filename(self.filename)))

    @staticmethod
    def secure_filename(filename) -> str:
        return filename.replace('//', '/').replace('\\', '/').rsplit('/', 1)[-1]

    @classmethod
    def create_avatar(cls, file) -> "Avatar": return cls(file)

    @property
    def file(self) -> FileStorage: return self.__file

    @property
    def is_valid(self) -> bool: return self.__valid

    @property
    def filename(self) -> str: return self.file.filename

    def __str__(self) -> str: return f"GravatarUpload(file={self.file}, status={self.status})"

    def __enter__(self): return self
    
    def __exit__(exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_type(exc_val)

    __repr__ = __str__
