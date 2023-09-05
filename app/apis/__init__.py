from app import api

from .followactions import *


api.add_resource(Follow, '/follow/<username>', endpoint='follow')
api.add_resource(Unfollow, '/unfollow/<username>', endpoint='unfollow')
api.add_resource(Followers, '/followers/<username>', endpoint='followers')
