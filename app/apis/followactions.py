# -*- encoding: utf-8 -*-
from typing import *
from collections import OrderedDict as ordered_dict
from abc import ABCMeta, abstractmethod
import json
import flask

from flask_restful import Resource
from flask_login import current_user

from app.models import BlogUser


__all__ = ['JSONResponse', 'auth_check', 'Unfollow', 'Follow', 'Followers']


JSONResponse = TypeVar('JSONResponse', bound=[MutableMapping[str, Optional[str | int]]])


def auth_check(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return UserRelationAPI.error_405()
        return func(*args, **kwargs)
    return wrapper


class UserRelationAPI(Resource, metaclass=ABCMeta):
    @abstractmethod
    @auth_check
    def get(self, *args, **kwargs): pass

    @abstractmethod
    @auth_check
    def post(self, *args, **kwargs): pass

    @staticmethod
    def noneless_dict(d: dict):
        keys = d.keys()
        [d.pop(k) for k in keys if not d.get(k)]
        return d

    def parse_valid_args(self, parser=None):
        parser = parser or self.parser
        args = parser.parse_args()
        args = self.noneless_dict(args)
        return args

    def ok_200(self, message=None) -> JSONResponse:
        return {
            'status': 200, 
            'reason': 'OK', 
            'message': message
        }

    def error_404(self, message) -> JSONResponse:
        return {
            'status': 404,
            'reason': 'Not Found',
            "message": message
        }

    @staticmethod
    def error_405() -> JSONResponse:
        return {
            'status': 405,
            'reason': 'You are not allowed to do that',
            'message': None
        }


class Follow(UserRelationAPI):
    @auth_check
    def get(self, username) -> MutableMapping:
        following_dict = {}
        for following_user in BlogUser.get_uuser(username=username).following:
            following_dict.update(following_user.to_dict(followers=False, following=False))
        return following_dict

    @auth_check
    def post(self, username):
        if not (target_user := BlogUser.get_uuser(username=username)):
            return self.error_404('User not found, please retry.')

        if current_user.is_following(target_user):
            return self.ok_200(f'Already followed {target_user}')

        current_user.follow(target_user).commit()

        return flask.redirect(flask.url_for('profile', username=username))


class Unfollow(UserRelationAPI):
    def get(self, username) -> JSONResponse:
        return self.error_405()

    @auth_check
    def post(self, username):
        if not (target_user := BlogUser.get_uuser(username=username)):
            return self.error_404('User not found, please retry.')

        if not current_user.is_following(target_user):
            return self.ok_200(f'{target_user} is not in your following list')

        current_user.unfollow(target_user).commit()
        return flask.redirect(flask.url_for('profile', username=username))


class Followers(UserRelationAPI):
    @auth_check
    def get(self, username) -> MutableMapping:
        follower_dict = {}
        for follower in BlogUser.get_uuser(username=username).followers:
            follower_dict.update(follower.to_dict(following=False, followers=False))
        return follower_dict

    def post(self, *args, **kwargs) -> JSONResponse:
        return self.error_405()
