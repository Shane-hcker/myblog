# -*- encoding: utf-8 -*-
from typing import *
from werkzeug.security import generate_password_hash, check_password_hash


__all__ = ['SaltyPassword', 'SaltyStr']

from typing import TypeVar


class SaltyPassword(str):
    def is_(self, other: str) -> bool:
        """
        see ``isHashOf()``
        :param other: the password to compare with
        """
        return self.isHashOf(other)

    def isHashOf(self, other: str) -> bool:
        """
        check whether the instance is the hash of ``other``
        using ``check_password_hash()``
        :param other: the password to compare with
        """
        return check_password_hash(self, other)

    @classmethod
    def wrap(cls, saltypassword: str) -> Self:
        """
        wraps salty password with ``SaltyPassword``
        :param saltypassword: saltypassword to wrap
        """
        return cls(saltypassword)

    @classmethod
    def saltify(cls, original: str) -> Self:
        """
        saltify a password with ``SaltyPassword()``
        :param original: the original password
        """
        return cls(generate_password_hash(original))


SaltyStr = TypeVar('SaltyStr', SaltyPassword, str)
