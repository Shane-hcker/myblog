# -*- encoding: utf-8 -*-
from typing import *
from collections import OrderedDict as ordered_dict
from abc import ABCMeta, abstractmethod
import json
import flask

from flask_restful import Resource
from flask_login import current_user

from app import api
from app.models import BlogUser


JSONResponse = TypeVar('JSONResponse', bound=[MutableMapping[str, Optional[Any]]])


def auth_check(func):
    def wrapper(*args, **kwargs) -> Any:
        if not current_user.is_authenticated:
            return UserRelationAPI.error_405()
        return func(*args, **kwargs)
    return wrapper


class UserRelationAPI(Resource, metaclass=ABCMeta):
    @abstractmethod
    @auth_check
    def get(self, *args, **kwargs) -> None: pass

    @abstractmethod
    @auth_check
    def post(self, *args, **kwargs) -> None: pass

    @staticmethod
    def noneless_dict(d: dict) -> Dict[Any, Any]:
        keys = d.keys()
        [d.pop(k) for k in keys if not d.get(k)]
        return d

    def parse_valid_args(self, parser=None) -> Dict[Any, Any]:
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
            'reason': 'OK', 
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
        following = BlogUser.get_uuser(username=username).following

        return {
            following_user.to_dict(followers=False, following=False)
            for following_user in following
        }

    @auth_check
    def post(self, username) -> JSONResponse | Any:
        """
        /follow/<username> POST
        """
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
    def post(self, username) -> JSONResponse | Any:
        if not (target_user := BlogUser.get_uuser(username=username)):
            return self.error_404('User not found, please retry.')

        if not current_user.is_following(target_user):
            return self.ok_200(f'{target_user} is not in your following list')

        current_user.unfollow(target_user).commit()
        return flask.redirect(flask.url_for('profile', username=username))


class Followers(UserRelationAPI):
    @auth_check
    def get(self, username) -> MutableMapping:
        followers_ = BlogUser.get_uuser(username=username).followers

        return {
            follower.to_dict(followers=False, following=False)
            for follower in followers_
        }

    def post(self, *args, **kwargs) -> JSONResponse:
        return self.error_405()


api.add_resource(Follow, '/follow/<username>', endpoint='follow')
api.add_resource(Unfollow, '/unfollow/<username>', endpoint='unfollow')
api.add_resource(Followers, '/followers/<username>', endpoint='followers')
