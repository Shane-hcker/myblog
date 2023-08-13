# -*- encoding: utf-8 -*-
from typing import *

from flask_restful import Resource, reqparse

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

    def parse_valid_args(self):
        args = self.parser.parse_args()
        keys = args.keys()
        [args.pop(k) for k in keys if not args.get(k)]
        return args

    def delete(self):
        """
        /follow DELETE
        form data: {'username': ..., 'email': ...}
        """
        target_user = BlogUser.get_uuser(**self.parse_valid_args())
        message = self.json_response(
            success=True,
            unfollowed=True
        )
        return {
            'target': target_user,
            'message': message
        }

    def post(self) -> Dict[str, Any]:
        """
        /follow POST
        form data: {'username': ..., 'email': ...}
        """
        target_user = BlogUser.get_uuser(**self.parse_valid_args())

        message = self.json_response(
            success=True,
            followed=True
        )

        return {
            'target': str(target_user), 
            'message': message
        }


api.add_resource(Follow, '/follow')
