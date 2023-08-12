# -*- encoding: utf-8 -*-
from typing import *
import json
import requests

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
    
    # @staticmethod
    # def status(status: int, reason='') -> Dict[str, Any]:
    #     return {
    #         'status': status, 
    #         'reason': reason
    #     }

    def post(self) -> Dict[str, Any]:
        args = self.parser.parse_args()
        print(args)
        return {
            'status': 200, 
            'reason': 'OK'
        }


api.add_resource(Follow, '/follow')
