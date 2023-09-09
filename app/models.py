# -*- encoding: utf-8 -*-
from typing import *
from collections import OrderedDict as ordered_dict
from datetime import datetime
import logging

from sqlalchemy import VARCHAR, Integer, DateTime, Text, select, and_
from sqlalchemy.orm import backref

# Plugins
from flask_login import UserMixin
from flask_wtf import FlaskForm

from app import db, login_manager, current_time, AppConfig
from app.utils.saltypassword import *
from app.utils.avatar import *
from app.utils.mixins import *
from app.datatypes import *


__all__ = ['BlogUser', 'Posts', 'retrieve_user', 'follow_table']


# load user from session
@login_manager.user_loader
def retrieve_user(user_id):
    # primary key -> id
    return BlogUser(False).get(int(user_id))


# creating association table
follow_table = db.Table(
    'follow_table',
    Column('follower_id', Integer, ForeignKey('userdata.id')),
    Column('following_id', Integer, ForeignKey('userdata.id'))
)


UserMapping = TypeVar('UserMapping', bound=Dict[str, Dict[str, Any]])


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
    email = Column(VARCHAR(64), unique=True, nullable=True)
    username = Column(VARCHAR(52), unique=True, nullable=True)
    avatar = Column(VARCHAR(128), nullable=True)
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
        'BlogUser', secondary=follow_table,
        primaryjoin=(follow_table.c.follower_id == id),
        secondaryjoin=(follow_table.c.following_id == id),
        backref=backref('followers', lazy=True),
        lazy=True
    )

    def __init__(self, user=True, *, email=None, username=None, avatar=None, password=None):
        if not user:
            return

        self.email = email
        self.username = username
        self.password = password
        self.avatar = avatar or Avatar.default_avatar()

    def to_dict(self, keyname=None, followers=True, following=True) -> UserMapping:
        user_dict = ordered_dict({
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'recent_login': self.recent_login,
        })
        user_dict.update({'followers': self.followers}) if followers else ...
        user_dict.update({'following': self.following}) if following else ...

        return ordered_dict({keyname or self.username: user_dict})

    def set_avatar(self, size=None, image=None) -> str:
        with Avatar(image or AppConfig.DEFAULT_AVATAR) as avatar:
            self.avatar = avatar.resize(size or 70).src.rsplit('/', 1)[-1]
            return self.avatar

    def reset_recent_login(self):
        self.recent_login = current_time()
        self.commit()

    @classmethod
    def add_user(cls, *args, **kwargs) -> "BlogUser":
        return cls(*args, **kwargs)

    @staticmethod
    def all_users(*params) -> List[Dict[str, Any]]:
        """ Mem efficient
        >>> list(BlogUser.all_users('*'))
        [BlogUser(username=..., email=...), ...]
        >>> list(BlogUser.all_users('username'))
        [{username: 'username'}, ...]
        """
        if '*' in params:
            return (yield from BlogUser(False).all())

        for user in BlogUser(False).all():
            user_dict = dict()
            for p in params:
                try:
                    user_dict.update({p: eval(f'user.{p}')})
                except Exception as e:
                    logging.error(e)
                    continue
            yield user_dict

    @staticmethod
    def get_uuser(**kwargs) -> "BlogUser":
        """
        get unique user
        """
        where_clause = and_(
            eval(f'BlogUser.{k} == \'{v}\'') for k, v in kwargs.items()
        )
        return db.session.scalar(select(BlogUser).where(where_clause))

    def visible_posts(self):
        """
        obtains posts of the user and user-subscribed users
        """
        user_posts = next(self.get_user_posts(raw=True))
        yield from (
            # join(association table, condition)
            Posts.query
            .join(follow_table, (follow_table.c.following_id == Posts.poster_id))
            .filter(follow_table.c.follower_id == self.id)
            .union(user_posts)
            .order_by(Posts.post_time.desc())  # desc() -> column method
        )

    def follow(self, *users: "BlogUser") -> Self:
        """
        >>> admin = BlogUser.get_uuser(id=1)
        >>> admin.follow(user1, user2)
        """
        [self.following.append(user) for user in users if not self.is_following(user)]
        return self

    def unfollow(self, *users: "BlogUser") -> Self:
        [self.following.remove(user) for user in users if self.is_following(user)]
        return self

    def is_following(self, user: "BlogUser") -> bool:
        return user in self.following

    @staticmethod
    def is_user_valid(form: FlaskForm, user: "BlogUser") -> bool:
        return user and user.password.isHashOf(form.password.data) and user.email == form.email.data.strip()

    @staticmethod
    def __parse_post(post: "Posts") -> Dict[str, str]:
        return {
            'poster': post.poster.username,
            'content': post.content,
            'date': post.post_time
        }

    def check_pwd(self, other) -> bool:
        return self.password.isHashOf(other)

    def get_user_posts(self, raw=False):
        if raw:
            yield Posts().filter_by(poster=self)
        else:
            yield from map(self.__parse_post,
                Posts().filter_by(poster=self).all()
            )

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
