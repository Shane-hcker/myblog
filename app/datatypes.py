# -*- encoding: utf-8 -*-
from typing import *
from io import TextIOWrapper

from sqlalchemy import TypeDecorator, VARCHAR
from app.utils.saltypassword import SaltyPassword
from app import db


__all__ = ['SaltyVarChar', 'Column', 'ForeignKey', 'FileLike']


Column = db.Column
ForeignKey = db.ForeignKey
FileLike = TypeVar('FileLike', TextIOWrapper, str)


class SaltyVarChar(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect) -> Optional[str]:
        return value

    def process_result_value(self, value, dialect) -> SaltyPassword:
        return SaltyPassword(value)
