from app import api

from .followactions import *
from .avataractions import *


api.add_resource(Follow, '/api/string:<username>/follow', endpoint='follow')
api.add_resource(Unfollow, '/api/<string:username>/unfollow', endpoint='unfollow')
api.add_resource(Followers, '/api/<string:username>/follower', endpoint='followers')

api.add_resource(AvatarAPI, '/api/avatar/<string:avatar>', endpoint='avatar')
