# -*- encoding: utf-8 -*-
from typing import *
from functools import partial
from datetime import datetime
import logging

from sqlalchemy import (VARCHAR, Integer, DateTime, Text, select, and_)
from sqlalchemy.orm import backref

# Plugins
from flask_login import (UserMixin)
from flask_wtf import FlaskForm
from flask_sqlalchemy.query import Query

from app import db, login_manager, current_time, forEach
from app.datatypes import *
from app.security.saltypassword import *
from app.utils.gravatar import *


__all__ = ['BlogUser', 'Posts', 'retrieve_user']


# load user from session
@login_manager.user_loader
def retrieve_user(user_id):
    # primary key -> id
    return BlogUser.query.get(int(user_id))


# creating association table
followers = db.Table(
    'followers',
    Column('follower_id', Integer, ForeignKey('userdata.id')),
    Column('following_id', Integer, ForeignKey('userdata.id'))
)


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

    def get(self, *args, **kwargs) -> Self:
        return self.query.get(*args, **kwargs)


class BlogUser(UserMixin, DBMixin, db.Model):  # One
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
    avatar = Column(VARCHAR(128), nullable=True, default=partial(default_avatar, email=email))
    password: SaltyStr = Column(SaltyVarChar(102), nullable=True)
    recent_login = Column(DateTime, nullable=True, default=datetime.now)

    # relationship() |>
    # view of relationship bt/ two tables
    # not an actual field in the table

    # backref --> field that's about to add to the `many` side(Posts)
    # lazy --> not running until explicit queries
    posts = db.relationship('Posts', backref='poster', lazy=True)

    # setting up following
    following = db.relationship(
        'BlogUser', secondary=followers, lazy=True,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=backref('followers', lazy=True),
    )

    def set_avatar(self, size=100, default=None) -> None:
        with GravatarFetcher(self.email, default or 'mp') as fetcher:
            self.avatar = fetcher.fetch(size).url

    def reset_recent_login(self):
        self.recent_login = current_time()
        self.commit()

    @staticmethod
    def fetch_all_users(*params) -> List[Dict[str, Any]]:
        """
        >>> BlogUser.fetch_all_users('username', ...)
        """
        res = []
        for user in BlogUser.query.all():
            user_dict = {}
            for p in params:
                try:
                    user_dict.update({p: eval(f'user.{p}')})
                except Exception as e:
                    logging.error(e)
                    continue
            res.append(user_dict)
        return res

    @staticmethod
    def get_uuser(**kwargs) -> "BlogUser":
        where_clause = and_(
            eval(f'BlogUser.{k} == \'{v}\'') for k, v in kwargs.items()
        )
        return db.session.scalar(select(BlogUser).where(where_clause))

    @staticmethod
    def isUserValid(form: FlaskForm, user: "BlogUser") -> bool:
        return user and user.password.isHashOf(form.password.data) and user.email == form.email.data.strip()

    @staticmethod
    def __parse_post(post: "Posts"):
        return {
            'author': post.poster.username,
            'content': post.content,
            'date': post.post_time
        }

    def check_pwd(self, other) -> bool:
        return self.password.isHashOf(other)

    def getUserPosts(self) -> List[Dict[str, Any]]:
        return forEach(Posts.query.filter_by(poster=self).all(), self.__parse_post)

    def follows(self, *users):
        """
        >>> admin = BlogUser.get_uuser(id=1)
        >>> admin.follows(user1, user2)
        """
        for user in users:
            # TODO
            ...

    def __str__(self) -> str:
        return f"BlogUser(username={self.username}, email={self.email})"

    __repr__ = __str__


class Posts(DBMixin, db.Model):  # Many
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    post_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    poster_id = Column(Integer, ForeignKey('userdata.id'))

    def __str__(self):
        return f"Posts(content={self.content},post_time={self.post_time})"

    __repr__ = __str__
