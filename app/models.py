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

from app import db, login_manager, current_time, forEach
from app.security.saltypassword import *
from app.utils.gravatar import *
from app.utils.mixins import *
from app.datatypes import *


__all__ = ['BlogUser', 'Posts', 'retrieve_user', 'followers']


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
        'BlogUser', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=backref('followers', lazy=True),
        lazy=True
    )

    def __init__(self, *, email, username, avatar=None, password=None):
        self.email = email
        self.username = username
        self.avatar = avatar
        self.password = password

    def set_avatar(self, size=100, default=None) -> None:
        with GravatarFetcher(self.email, default or 'mp') as fetcher:
            self.avatar = fetcher.fetch(size).url

    def reset_recent_login(self):
        self.recent_login = current_time()
        self.commit()

    @staticmethod
    def get_all_users(*params) -> List[Dict[str, Any]]:
        """
        >>> BlogUser.get_all_users('username')
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
        """
        get unique user
        """
        where_clause = and_(
            eval(f'BlogUser.{k} == \'{v}\'') for k, v in kwargs.items()
        )
        return db.session.scalar(select(BlogUser).where(where_clause))

    def get_visible_posts(self):
        """
        obtains posts of the user and user-subscribed users
        """
        user_posts = self.get_user_posts()
        return (
            # join(association table, condition)
            Posts()
            .join(followers, followers.c.following_id == Posts.poster_id)
            .filter(followers.c.follower_id == self.id)
            .union(user_posts)
            .order_by(Posts.post_time.desc())  # desc() -> column method
        )

    def follows(self, *users: Iterable["BlogUser"]) -> Self:
        """
        >>> admin = BlogUser.get_uuser(id=1)
        >>> admin.follows(user1, user2)
        """
        [self.following.append(user) for user in users]
        return self.commit()

    def unfollows(self, *users: Iterable["BlogUser"]) -> Self:
        [self.following.remove(user) for user in users]
        return self.commit()

    def is_following(self, user: "BlogUser") -> bool:
        return user in self.following

    @staticmethod
    def is_user_valid(form: FlaskForm, user: "BlogUser") -> bool:
        return user and user.password.isHashOf(form.password.data) and user.email == form.email.data.strip()

    @staticmethod
    def __parse_post(post: "Posts") -> Dict[str, str]:
        return {
            'author': post.poster.username,
            'content': post.content,
            'date': post.post_time
        }

    def check_pwd(self, other) -> bool:
        return self.password.isHashOf(other)

    def get_user_posts(self) -> List[Dict[str, Any]]:
        return forEach(Posts.query.filter_by(poster=self).all(), self.__parse_post)

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
