# -*- encoding: utf-8 -*-
from typing import *

import flask
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_login import login_required, current_user

from app.models import Posts, BlogUser


class SearchAPI(Resource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = (RequestParser()
                       .add_argument('q', type=str, location='args'))

    @login_required
    def get(self):
        if not (query := self.parser.parse_args().get('q')):
            return {
                'status': 405,
                'reason': 'You are not allowed to do that',
                'message': None
            }
        return {
            'status': 200,
            'reason': 'OK',
            'message': {
                'user': {},
                'post': {}
            }
        }