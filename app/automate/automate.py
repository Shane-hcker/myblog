# -*- encoding: utf-8 -*-
from typing import *
import random

from context import *
from app import db
from app.models import *
from app.security.saltypassword import *


@app_context
class BuildUser:
    def build_user(self):
        ...

    def build_posts(self):
        ...

    def build_user_relation(self):
        ...

    def build(self):
        ...