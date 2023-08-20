# -*- encoding: utf-8 -*-
from typing import *
from abc import ABCMeta, abstractmethod
import flask

from flask_restful import Resource, reqparse
from flask_login import current_user, login_required

from app import api
from app.models import BlogUser


class UserRelationAPI(Resource, metaclass=ABCMeta):
    @abstractmethod
    def get(self) -> None: pass

    @abstractmethod
    def post(self) -> None: pass

    @abstractmethod
    def delete(self) -> None: pass


class Following(UserRelationAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fusername', type=str, location='form')
        self.parser.add_argument('femail', type=str, location='form')

    @login_required
    def get(self, username):
        if current_user.username != username:
            return self.error_405()

    @login_required
    def delete(self, username):
        """
        /follow DELETE
        form data: {'fusername': ..., 'femail': ...}
        """
        if current_user.username != username:
            return self.error_405()

        if not (data := self.parse_valid_args()):
            return self.error_400()

        if not current_user.is_following(target_user := BlogUser.get_uuser(**data)):
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

    @login_required
    def post(self, username) -> Dict[str, Any]:
        """
        /follow POST
        form data: {'fusername': ..., 'femail': ...}
        """
        if current_user.username != username:
            return self.error_405()

        if not (data := self.parse_valid_args()):
            return self.error_400()

        target_user = BlogUser.get_uuser(**data)

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

    @staticmethod
    def error_400():
        return {
            "status": 400,
            "reason": 'Missing parameters',
            'message': None
        }

    @staticmethod
    def error_405():
        return {
            'status': 405,
            'reason': 'You are not allowed to do that',
            'message': None
        }

    def parse_valid_args(self, parser=None):
        parser = parser or self.parser
        args = parser.parse_args()
        args = self.noneless_dict(args)
        return args

    @staticmethod
    def noneless_dict(d: dict):
        keys = d.keys()
        [d.pop(k) for k in keys if not d.get(k)]
        return d


class Follower(UserRelationAPI):
    pass


# api.add_resource(Follower, '/<username>/follower', endpoint='follower')
api.add_resource(Following, '/<username>/following', endpoint='following')
