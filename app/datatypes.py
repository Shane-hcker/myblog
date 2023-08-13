# -*- encoding: utf-8 -*-
from typing import *
from sqlalchemy import TypeDecorator, VARCHAR
from app.utils.saltypassword import SaltyPassword
from app import db

__all__ = ['SaltyVarChar', 'Column', 'ForeignKey']


Column = db.Column
ForeignKey = db.ForeignKey


class SaltyVarChar(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect) -> Optional[str]:
        return value

    def process_result_value(self, value, dialect) -> SaltyPassword:
        return SaltyPassword(value)
