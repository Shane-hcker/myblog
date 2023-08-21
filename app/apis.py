# -*- encoding: utf-8 -*-
from typing import *
from abc import ABCMeta, abstractmethod
import flask

from flask_restful import Resource, reqparse
from flask_login import current_user, login_required

from app import api
from app.models import BlogUser


JSONResponse = TypeVar('JSONResponse', bound=[Dict[str, Optional[Any]]])


def auth_check(func):
    def wrapper(*args, **kwargs):
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
    def error_405() -> JSONResponse:
        return {
            'status': 405,
            'reason': 'You are not allowed to do that',
            'message': None
        }

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


class Follow(UserRelationAPI):
    @auth_check
    def get(self, username) -> JSONResponse:
        following = BlogUser.get_uuser(username=username).following

        return {
            f'user{i}': {
                'username': (user := following[i]).username,
                'email': user.email,
                'avatar': user.avatar,
            }
            for i in range(len(following))
        }

    @auth_check
    def post(self, username) -> JSONResponse:
        """
        /follow/<username> POST
        """
        if not (target_user := BlogUser.get_uuser(username=username)):
            return {
                'status': 404,
                'reason': 'Not Found',
                'message': 'User not found, please retry.'
            }

        if current_user.is_following(target_user):
            return {
                'status': 200,
                'reason': 'OK',
                'message': f'Already followed {target_user}'
            }

        current_user.follow(target_user).commit()

        # flask.redirect(flask.url_for('profile', username=username))

        return {
            'status': 200,
            'reason': 'OK',
            'message': f'Followed {str(target_user)}'
        }


class Unfollow(UserRelationAPI):
    def get(self, username) -> Dict[str, str | int]:
        return self.error_405()

    @auth_check
    def post(self, username) -> JSONResponse:
        if not (target_user := BlogUser.get_uuser(username=username)):
            return {
                'status': 404,
                'reason': 'Not Found',
                'message': 'User not found, please retry.'
            }

        if not current_user.is_following(target_user):
            return {
                'status': 200,
                'reason': 'OK',
                'message': f'{target_user} is not in your following list'
            }

        current_user.unfollow(target_user).commit()
        # flask.redirect(flask.url_for('profile', username=username))
        return {
            'status': 200,
            'reason': 'OK',
            'message': f'Followed {str(target_user)}'
        }


class Followers(UserRelationAPI):
    @auth_check
    def get(self, username) -> JSONResponse:
        followers = BlogUser.get_uuser(username=username).followers

        return {
            f'user{i}': {
                'username': (user := followers[i]).username,
                'email': user.email,
                'avatar': user.avatar,
            }
            for i in range(len(followers))
        }

    def post(self, *args, **kwargs) -> JSONResponse:
        return self.error_405()


api.add_resource(Follow, '/follow/<username>', endpoint='follow')
api.add_resource(Unfollow, '/unfollow/<username>', endpoint='unfollow')
api.add_resource(Followers, '/followers/<username>', endpoint='follower')
