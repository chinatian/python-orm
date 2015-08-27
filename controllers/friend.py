#-*- coding: utf8 -*-

from controllers import authenticated
from controllers import BaseHandler
from models.user import User, UserDetail, UserIndex
from models.friend import Friend
try:
    import simplejson as json
except ImportError:
    import json

class MyFriendsHandler(BaseHandler):
    @authenticated
    def get(self):
        me = self.get_current_user()
        users = []
        fus = Friend.get_friend_users(me.id)
        for fu in fus:
            users.append(dict(id=fu.id, name=fu.name, head_img_url=fu.head_img_url))
        result = {'success':True, 'users':users}
        self.write(json.dumps(result))
