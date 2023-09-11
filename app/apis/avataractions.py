# -*- encoding: utf-8 -*-
from typing import *

from flask import url_for
import base64
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app import AppConfig
from app.utils.avatar import *


__all__ = ['AvatarAPI']


class AvatarAPI(Resource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.parser = (RequestParser()
                       .add_argument('username', type=str, location='args'))

    def get(self, avatar) -> MutableMapping:
        return {
            'avatar': url_for('static', filename=f'{AppConfig.AVATAR_DIR}/{avatar}')
        }

    def post(self, avatar: str) -> None:
        with Avatar(raw=base64.b64decode(avatar.encode('utf-8'))) as f:
            f.save(f'../static{AppConfig.AVATAR_DIR}/{self.parser.parse_args()["username"]}.png')
