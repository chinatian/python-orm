#!/usr/bin/env python
#-*- coding: utf8 -*-

import os.path
import hashlib
from models.user import User, UserDetail, UserIndex
from models.friend import Friend
from datetime import datetime
try:
    import simplejson as json
except ImportError:
    import json

def load():
    file_path = os.path.join(os.path.dirname(__file__), 'test_data.json')
    f = open(file_path, 'r')
    content = f.read().decode('utf8')
    f.close()
    data = json.loads(content)
    users = data['users']
    friends = data['friends']
    for user in users:
        pw_md5 = hashlib.md5()
        pw_md5.update(user['password'])
        u = User(name=user['name'], password=pw_md5.hexdigest(), head_img_url=user['head_img_url'], last_login_time=datetime.now())
        u.insert()
        for detail in user['user_details']:
            ud = UserDetail(user_id=u.id, field_name=detail['field_name'], field_value='%s,v' % detail['field_value'], updated_at=datetime.now())
            ud.insert()
            ui = UserIndex(field_name=detail['field_name'], field_value=detail['field_value'], user_id=u.id)
            ui.insert()
    for friend in friends:
        user_id = UserIndex.get_user_id('phone', friend['user_phone'])
        friend_id = UserIndex.get_user_id('phone', friend['friend_phone'])
        f = Friend(user_id=user_id, friend_id=friend_id)
        f.insert()
        print "u_id: %d, f_id: %d" % (user_id, friend_id)
        f = Friend(user_id=friend_id, friend_id=user_id)
        f.insert()
        print "u_id: %d, f_id: %d" % (friend_id, user_id)

        