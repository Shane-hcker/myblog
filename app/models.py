# -*- encoding: utf-8 -*-
from typing import *
from datetime import datetime
from sqlalchemy import (VARCHAR, Integer, DateTime, Text)

from app import db
from .datatypes import *


class BlogUser(db.Model):  # One
    """ Main Table
    flask db init |>
    -> flask db migrate
    -> create database, then:
    -> flask db upgrade
    """
    __tablename__ = 'userdata'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(64), unique=True, nullable=False)
    username = Column(VARCHAR(52), unique=True, nullable=False)
    salty_password = Column(SaltyVarChar(102), nullable=True)
    recent_login = Column(DateTime, nullable=True, default=datetime.now)

    # relationship() |>
    # view of relationship bt/ two tables
    # not an actual field in the table

    # backref --> field that's about to add to the Many side(Posts)
    posts = db.relationship('Posts', backref='poster', lazy=True)

    def __str__(self):
        return f"BlogUser(username={self.username}, email={self.email})"

    __repr__ = __str__


class Posts(db.Model):  # Many
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    post_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    poster_id = Column(Integer, ForeignKey('userdata.id'))

    def __str__(self):
        return f"{self.content}"

    __repr__ = __str__
