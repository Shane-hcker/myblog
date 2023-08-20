# -*- encoding: utf-8 -*-
from typing import *
from abc import ABCMeta, abstractmethod
import flask

from flask_restful import Resource, reqparse
from flask_login import current_user, login_required

from app import api
from app.models import BlogUser


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

    @abstractmethod
    @auth_check
    def delete(self, *args, **kwargs) -> None: pass

    @staticmethod
    def error_405():
        return {
            'status': 405,
            'reason': 'You are not allowed to do that',
            'message': None
        }

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


class Following(UserRelationAPI):
    @auth_check
    def get(self, username):
        """
        /follow/<username> GET
        return a list of <username> followed users
        """
        following = BlogUser.get_uuser(username=username).following

        return {
            f'user{i}': following[i]
            for i in range(len(following))
        }


    @auth_check
    def delete(self, username):
        """
        /follow/<username> DELETE
        """
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
                'message': f'Already followed {target_user}'
            }

        current_user.unfollow(target_user)

        return {
            'status': 200,
            'reason': 'OK',
            'message': f'Unfollowed {target_user}'
        }

    @auth_check
    def post(self, username) -> Dict[str, Any]:
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

        current_user.follow(target_user)

        return {
            'status': 200,
            'reason': 'OK',
            'message': f'Followed {str(target_user)}'
        }


class Follower(UserRelationAPI):
    pass


api.add_resource(Follower, '/follower/<username>', endpoint='follower')
api.add_resource(Following, '/following/<username>', endpoint='following')
