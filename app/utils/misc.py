# -*- encoding: utf-8 -*-
from typing import *
import os

# import flask
# from requests import post as rpost, delete as rdelete
# from flask_login import current_user
from werkzeug.datastructures import FileStorage

from app.models import Posts, BlogUser


__all__ = ['getAllPosts', 'flash_parse', 'is_file_allowed']


def getAllPosts() -> List[Dict[str, Any]]:
    return [
        {
            'poster': post.poster.username,
            'content': post.content,
            'post_time': post.post_time,
        } for post in Posts().all()
    ]


def flash_parse(flash_messages) -> Optional[List[str]]:
    parse = lambda msg: [
        'success' if (msg_ := msg.split(';'))[0] == 'success'
        else 'error', msg_[-1]
    ]
    return map(parse, flash_messages) if flash_messages else []


def is_file_allowed(file: FileStorage, allow_ext: Iterable) -> bool:
        return '.' in file.filename and os.path.splitext(file.filename)[-1].lower() in allow_ext
