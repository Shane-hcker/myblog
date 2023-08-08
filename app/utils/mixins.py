# -*- encoding: utf-8 -*-
from typing import *

from app import db


__all__ = ['DBMixin']


class DBMixin:
    def __getattr__(self, item):
        return eval(f"self.query.{item}")

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
