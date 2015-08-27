#-*- coding: utf8 -*-

import functools
import tornado.web

from models.user import User
from tornado.web import HTTPError

def authenticated(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.set_status(403)
            return
        return method(self, *args, **kwargs)
    return wrapper

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return User.get(long(user_id))

class HomeHandler(BaseHandler):
    def get(self):
        self.write("Rekoo Social Game Platform")
