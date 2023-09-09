# -*- encoding: utf-8 -*-
from typing import *
from flask_restful import Resource


class Image(Resource):
    def get(self, image) -> MutableMapping:
        try:
            with open(f'../static/avatar/{image}', 'rb') as img:
                return {
                    'status': 200,
                    'reason': 'OK',
                    'img_stream': str(img.read())
                }
        except FileNotFoundError:
            return {
                'status': 404,
                'reason': 'Not Found',
                'message': 'Image does not exist'
            }
