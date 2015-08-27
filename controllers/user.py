#-*- coding: utf8 -*-

import hashlib
from controllers import authenticated
from controllers import BaseHandler
from models.user import User, UserDetail, UserIndex
from datetime import datetime
try:
    import simplejson as json
except ImportError:
    import json

class SignUpHandler(BaseHandler):
    def get(self):
        data = {'success':True, 'user':{'id':12345, 'password':'666666'}}
        self.write(json.dumps(data))
    def post(self):
        name = self.get_argument("name")
        phone = self.get_argument("phone", None)
        # 保存数据
        pw = '123456'
        pw_md5 = hashlib.md5()
        pw_md5.update(pw)
        u = User(name=name, password=pw_md5.hexdigest(), last_login_time=datetime.now())
        u.insert()
        if phone:
            ud = UserDetail(user_id=u.id, field_name='phone', field_value='%s,v' % phone, updated_at=datetime.now())
            ud.insert()
            ui = UserIndex(field_name='phone', field_value=phone, user_id=u.id)
            ui.insert()
            result = {'success':True, 'user':{'id':u.id, 'password':pw}}
        else:
            result = {'success':True}
        self.set_secure_cookie("user", str(u.id))
        self.write(json.dumps(result))

class SignUpPhoneHandler(BaseHandler):
    @authenticated
    def post(self):
        phone = self.get_argument("phone")
        u = self.get_current_user()
        pw = '123456'
        pw_md5 = hashlib.md5()
        pw_md5.update(pw)
        u.password = pw_md5.hexdigest()
        u.update()
        ud = UserDetail(user_id=u.id, field_name='phone', field_value='%s,v' % phone, updated_at=datetime.now())
        ud.insert()
        ui = UserIndex(field_name='phone', field_value=phone, user_id=u.id)
        ui.insert()
        result = {'success':True, 'user':{'id':u.id, 'password':pw}}
        self.write(json.dumps(result))

class SignUpPasswordHandler(BaseHandler):
    @authenticated
    def post(self):
        password = self.get_argument("password")
        u = self.get_current_user()
        pw_md5 = hashlib.md5()
        pw_md5.update(password)
        u.password = pw_md5.hexdigest()
        u.update()
        result = {'success':True}
        self.write(json.dumps(result))
