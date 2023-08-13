# -*- encoding: utf-8 -*-
from typing import *

from flask_restful import Resource, reqparse

from app import api
from app.models import BlogUser, Posts


class Follow(Resource):
    """
    /follow
    POST {'username': ..., }
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, location='form')
        self.parser.add_argument('email', type=str, location='form')

    @staticmethod
    def response_msg(success: bool) -> Dict[str, Any]:
        return {
            'success': success
        }

    def post(self) -> Dict[str, Any]:
        data_args = self.parser.parse_args()
        keys = data_args.keys()
        [data_args.pop(k) for k in keys if not data_args.get(k)]
        target_user = BlogUser.get_uuser(**data_args)

        return {
            'target': str(target_user), 
            'message': self.response_msg(success=True)
        }


api.add_resource(Follow, '/follow')
