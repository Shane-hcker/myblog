# -*- encoding: utf-8 -*-
from typing import *

from app.models import Posts, BlogUser
from app import forEach


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
    return forEach(flash_messages, parse, ret_val=True) if flash_messages else []
