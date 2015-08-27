#-*- coding: utf8 -*-

import re
import hashlib
from controllers import BaseHandler
from models.user import User, UserDetail, UserIndex
try:
    import simplejson as json
except ImportError:
    import json

class LoginHandler(BaseHandler):
    def get(self):
        self.write("get Login")
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        pw_md5 = hashlib.md5()
        pw_md5.update(password)
        md5_pw = pw_md5.hexdigest()
        u = None
        if re.match(r"\A\d{1,19}\Z", username):#手机号码或rekoo号
            u = auth_user_id(username, md5_pw)
            if (not u) and len(username) == 11:
                u = auth_phone(username, md5_pw)
        elif re.match(r"\A[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+\Z", username):#邮箱
            u = auth_email(username, md5_pw)
        if u:
            result = {'success':True, 'user':{'id':u.id, 'name':u.name}}
            self.set_secure_cookie("user", str(u.id))
        else:
            result = {'success':False}
        self.write(json.dumps(result))

def auth_user_id(username, md5_pw):
    try:
        u = User.get(long(username))
        if u.password == md5_pw:
            return u
    except:
        return None
    return None

def auth_phone(username, md5_pw):
    try:
        user_id = UserIndex.get_user_id('phone', username)
        u = User.get(user_id)
        if u.password == md5_pw:
            return u
    except:
        return None
    return None

def auth_email(username, md5_pw):
    try:
        user_id = UserIndex.get_user_id('email', username)
        u = User.get(user_id)
        if u.password == md5_pw:
            return u
    except:
        return None
    return None

class LogoutHandler(BaseHandler):
    def get(self):
        result = {'success':True}
        self.clear_cookie("user")
        self.write(json.dumps(result))