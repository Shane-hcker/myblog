# -*- encoding: utf-8 -*-
from typing import *
import flask

from flask_restful import Resource, reqparse
from flask_login import current_user, login_required

from app import api
from app.models import BlogUser


class Follow(Resource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('email', type=str, location='form')

    @staticmethod
    def json_response(success: bool, **kwargs) -> Dict[str, Any]:
        resp_json = {'success': success}
        resp_json.update({f'{k}': v for k, v in kwargs.items()})
        return resp_json

    @staticmethod
    def parse_valid_args(parser):
        args = parser.parse_args()
        keys = args.keys()
        [args.pop(k) for k in keys if not args.get(k)]
        return args

    @login_required
    def get(self):
        return {
            'user': None
        }

    @login_required
    def delete(self):
        """
        /follow DELETE
        form data: {'username': ..., 'email': ...}
        """
        target_user = BlogUser.get_uuser(**self.parse_valid_args())
        response = self.json_response(
            success=True,
            unfollowed=True
        )
        return {
            'following': target_user,
            'response': response
        }

    @login_required
    def post(self) -> Dict[str, Any]:
        """
        /follow POST
        form data: {'username': ..., 'email': ...}
        """
        if not (args := self.parse_valid_args(self.parser)):
            return {
                'following': None,
                'response': self.json_response(
                    success=False,
                    message='Missing `username` or `email` in form data'
                )
            }

        target_user = BlogUser.get_uuser(**args)

        response = self.json_response(
            success=True,
            message=f'successfully followed: {str(target_user)}'
        )

        return {
            'following': str(target_user),
            'response': response
        }


api.add_resource(Follow, '/follow')
