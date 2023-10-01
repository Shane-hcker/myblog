import flask

from app import api, app

from .followactions import *
from .avataractions import *


api.add_resource(Follow, '/api/string:<username>/follow', endpoint='follow')
api.add_resource(Unfollow, '/api/<string:username>/unfollow', endpoint='unfollow')
api.add_resource(Followers, '/api/<string:username>/follower', endpoint='followers')

api.add_resource(AvatarAPI, '/api/avatar/<string:avatar>', endpoint='avatar')

# app.add_url_rule('/api/avatar/<string:avatar>', endpoint='avatar', build_only=True)
