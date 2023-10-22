# -*- encoding: utf-8 -*-
from typing import *

import flask
from flask_restful import Resource
from flask_login import login_required, current_user


class SearchAPI(Resource):
    def post(self):
        