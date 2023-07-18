# -*- encoding: utf-8 -*-
from typing import *
from datetime import datetime
from sqlalchemy import (VARCHAR, Integer, DateTime, Text, select, and_)
from werkzeug.security import check_password_hash

# Plugins
from flask_login import (UserMixin, AnonymousUserMixin)
from flask_wtf import FlaskForm

from app import db, login_manager, current_time, forEach
from .datatypes import *
from .utils.saltypassword import *
from .utils.gravatar import *


__all__ = ['BlogUser', 'Posts', 'retrieve_user']


# load user from session
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

    def avatar(self, size=100):
        with GravatarFetcher(self.email) as fetcher:
            return fetcher.fetch(size)

    def reset_recent_login(self):
        self.recent_login = current_time()
        return db.session.commit()

    @staticmethod
    def __parse_post(post: "Posts"):
        return {
            'author': post.poster.username,
            'content': post.content,
            'date': post.post_time
        }

    def getUserPosts(self) -> List[Dict[str, Any]]:
        return forEach(Posts.query.filter_by(poster=self.username), self.__parse_post)

    @staticmethod
    def get_uuser(**kwargs) -> "BlogUser":
        where_clause = and_(
            eval(f'BlogUser.{k} == \'{v}\'') for k, v in kwargs.items()
        )
        return db.session.execute(select(BlogUser).where(where_clause)).first()

    @staticmethod
    def isUserValid(form: FlaskForm, user: "BlogUser") -> bool:
        return user and user.password.isHashOf(form.password.data) and user.email == form.email.data.strip()

    def check_pwd(self, other) -> bool:
        return self.password.isHashOf(other)

    def __str__(self):
        return f"BlogUser(username={self.username}, email={self.email})"

    @property
    def password(self) -> SaltyPassword: return self.salty_password

    @password.setter
    def password(self, value: str) -> None: self.salty_password = value

    __repr__ = __str__


class Posts(db.Model):  # Many
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    post_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    poster_id = Column(Integer, ForeignKey('userdata.id'))

    def __str__(self):
        return f"Posts(content={self.content},post_time={self.post_time})"

    __repr__ = __str__
