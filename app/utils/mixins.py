# -*- encoding: utf-8 -*-
from typing import *

from flask_sqlalchemy.query import Query

from app import db


__all__ = ['DBMixin']


class DBMixin:
    def flush(self) -> Self:
        db.session.flush()
        return self

    def commit(self) -> Self:
        db.session.commit()
        return self

    def add(self, instance: object, _warn: bool = True) -> Self:
        db.session.add(instance, _warn)
        return self

    def add_all(self, instances: Iterable[object]) -> Self:
        db.session.add_all(instances)
        return self

    def filter_by(self, *args, **kwargs) -> Query:
        return self.query.filter_by(*args, **kwargs)

    def get(self, *args, **kwargs) -> object:
        return self.query.get(*args, **kwargs)

    def all(self) -> List[object]:
        return self.query.all()
