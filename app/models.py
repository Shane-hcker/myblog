# -*- encoding: utf-8 -*-
from typing import *
from datetime import datetime
from sqlalchemy import (VARCHAR, Integer, DateTime, Text)
from werkzeug.security import check_password_hash

# Plugins
from flask_login import (UserMixin, AnonymousUserMixin)
from flask_wtf import FlaskForm

from app import db, login_manager, current_time
from .datatypes import *
from .utils.saltypassword import *


__all__ = ['BlogUser', 'Posts', 'retrieve_user']


@login_manager.user_loader
def retrieve_user(user_id):
    # primary key -> id
    return BlogUser.query.get(int(user_id))


class BlogUser(UserMixin, db.Model):  # One
    """ Main Table
    flask db init |>
    -> flask db migrate -m "msg"
    -> create database if doesn't exist, then:
    -> flask db upgrade/downgrade
    """
    __tablename__ = 'userdata'

    # id -> UserMixin.get_id()
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(64), unique=True, nullable=False)
    username = Column(VARCHAR(52), unique=True, nullable=False)
    salty_password: SaltyStr = Column(SaltyVarChar(102), nullable=True)
    recent_login = Column(DateTime, nullable=True, default=datetime.now)

    # relationship() |>
    # view of relationship bt/ two tables
    # not an actual field in the table

    # backref --> field that's about to add to the `many` side(Posts)
    posts = db.relationship('Posts', backref='poster', lazy=True)

    @staticmethod
    def get_uuser(**kwargs) -> "BlogUser":
        return BlogUser.query.filter_by(**kwargs).first()

    @staticmethod
    def isUserValid(form: FlaskForm, user: "BlogUser") -> bool:
        return user and user.password.isHashOf(form.password.data)

    def check_pwd(self, other) -> bool:
        return self.password.isHashOf(other)

    def __str__(self):
        return f"BlogUser(username={self.username}, email={self.email})"

    __repr__ = __str__

    @property
    def password(self) -> SaltyPassword: return self.salty_password

    @password.setter
    def password(self, value: str) -> None: self.salty_password = value

    def reset_recent_login(self, now=True):
        if now:
            self.recent_login = current_time()
            return
        self.recent_login = datetime(0)
        db.session.commit()


class Posts(db.Model):  # Many
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    post_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    poster_id = Column(Integer, ForeignKey('userdata.id'))

    @property
    def content_(self) -> str:
        return self.content

    @content_.setter
    def content_(self, value: str) -> None:
        self.content = value

    def __str__(self):
        return f"Posts(content={self.content},post_time={self.post_time})"

    __repr__ = __str__
