# -*- encoding: utf-8 -*-
from typing import *
import os
import hashlib
from urllib.parse import urlencode
import pickle

from werkzeug.utils import secure_filename
import requests

from app.datatypes import *
from app.exceptions import *

__all__ = ['Gravatar', 'default_avatar', 'Avatar']


class Avatar:
    def __init__(self, image: Optional[BufferedLike] = None) -> None:
        self.__raw: PickledBytes = self.pickled(image)

    @pickletyping
    def pickled(self, file: BufferedLike) -> Optional[PickledBytes]:
        # todo avatar completion + implementation in routes.py
        if isinstance(file, BufferedReader):
            return pickle.dumps(file.read())
        if isinstance(file, str):
            return self.__pickle_img(file)

    @staticmethod
    def __pickle_img(filename: str) -> bytes:
        """
        Only applicable to file with only path given
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f'{filename} does not exist')
        with open(filename, 'rb') as file:
            return pickle.dumps(file.read())

    @pickletyping
    def raw_from_file(self, file: BufferedLike):
        if isinstance(file, BufferedReader):
            return pickle.loads(file.read())
        if isinstance(file, str):
            with open(file, 'rb') as f:
                return pickle.loads(f.read())

    @property
    def raw(self) -> PickledBytes:
        return self.__raw

    @raw.setter
    def raw(self, raw) -> None:
        if isinstance(raw, bytes):
            self.__raw = raw
        elif isinstance(raw, (str, BufferedReader)):
            self.__raw = self.pickled(raw)
        else:
            raise ParamError('Wrong type for parameter `raw`, expected `BufferedLike` or `bytes`')


class Gravatar:
    URL = 'https://www.gravatar.com/avatar/'

    def __init__(self, file:Optional[BufferedLike] = None, *,
                 email:Optional[str] = None, default:str = 'mp') -> None:
        self.__file = file
        self.__email = email.strip() if email else None
        self.__default = default
        self.__gravatar_url = None

    def fetch(self, size=50) -> Self:
        if not isinstance(self.email, str):
            raise TypeError('Parameter `<Gravatar.__email>` should not be None')
        query = {'s': size or 50}
        query.update({'d': self.default or 'mp'})
        hashed = self.__hash_email(self.email)
        self.gravatar_url = f'{self.URL}{hashed}/?{urlencode(query)}'
        return self

    def request_image_url(self):
        pass

    def request_gravatar_url(self):
        pass

    @staticmethod
    def open(file: BufferedLike, mode:str = 'r') -> TextIO:
        if isinstance(file, str):
            return open(file, mode=mode)
        return file

    def save(self, filename) -> None:
        with open(filename, 'wb') as file:
            file.write(requests.get(self.gravatar_url).content)

    @staticmethod
    def __hash_email(email):
        if not email:
            raise TypeError(f'Parameter `<Gravatar.__email>` should be not None')
        return hashlib.md5(email.lower().encode()).hexdigest()

    @property
    def file(self) -> Optional[BufferedLike]:
        return self.__file

    @property
    def email(self) -> Optional[str]:
        return self.__email

    @property
    def gravatar_url(self) -> Optional[str]:
        return self.__gravatar_url

    @property
    def default(self) -> Optional[str]:
        return self.__default

    @file.setter
    def file(self, file: BufferedLike) -> None:
        self.__file = file

    @email.setter
    def email(self, email: str) -> None:
        self.__email = email

    @gravatar_url.setter
    def gravatar_url(self, gravatar_url: str) -> None:
        self.__gravatar_url = gravatar_url

    @default.setter
    def default(self, default: str) -> None:
        self.__default = default

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            raise exc_type(exc_val)

    def __str__(self) -> str:
        return self.gravatar_url

    __repr__ = __str__


def default_avatar(email, size=100) -> str:
    with Gravatar(email) as fetcher:
        return fetcher.fetch(size).gravatar_url


if __name__ == '__main__':
    avatar = Avatar(open('../static/avatar/user.png', 'rb'))
    with open('./images/haha.rnd', 'wb') as f_:
        avatar.raw.to_file(f_)
