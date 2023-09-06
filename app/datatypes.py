# -*- encoding: utf-8 -*-
import os.path
from typing import *
from functools import wraps
from io import BufferedWriter, BufferedReader
import pickle

from sqlalchemy import TypeDecorator, VARCHAR
from app.utils.saltypassword import SaltyPassword
from app import db


__all__ = [
    'SaltyVarChar', 'Column', 'ForeignKey', 'BufferedLike', 'PickledBytes',
    'pickletyping', 'BufferedWriter', 'BufferedReader'
]


Column = db.Column
ForeignKey = db.ForeignKey
BufferedLike = TypeVar('BufferedLike', str, BufferedWriter, BufferedReader, BinaryIO)


def pickletyping(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return PickledBytes(func(*args, **kwargs))
        except TypeError:
            return None
    return wrapper


class PickledBytes(bytes):
    def to_file(self, file: FileLike) -> None:
        if isinstance(file, str) and os.path.exists(file):
            with open(file, 'wb') as f:
                pickle.dump(self, f)
        elif isinstance(file, BufferedWriter):
            pickle.dump(self, file)


class SaltyVarChar(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect) -> Optional[str]:
        return value

    def process_result_value(self, value, dialect) -> SaltyPassword:
        return SaltyPassword(value)
