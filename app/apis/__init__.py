from app import api

from .followactions import *
from .avataractions import *


api.add_resource(Follow, f'/api/<username>/follow', endpoint='follow')
api.add_resource(Unfollow, '/api/<username>/unfollow', endpoint='unfollow')
api.add_resource(Followers, '/api/<username>/follower', endpoint='followers')
# api.add_resource(..., '/api/<username>/avatar', endpoint='avatar')

api.add_resource(AvatarAPI, '/api/avatar/<avatar>', endpoint='avatar')
