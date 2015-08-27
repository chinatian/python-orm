#!/usr/bin/env python
#-*- coding: utf8 -*-

from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase

import manage
import re

try:
    import simplejson as json
except ImportError:
    import json

class FriendTest(AsyncHTTPTestCase):
    def get_app(self):
        return manage.Application()
    
    def test_me_friends(self):
        response = self.fetch('/auth/login',
            method="POST",
            body="username=13811429668&password=123456")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        
        user_cookie = re.findall('user=([\w\|]+);', response.headers['Set-Cookie'])[0]
        print user_cookie
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        
        cookie = 'user=%s;' % user_cookie
        
        response = self.fetch('/me/friends',
            headers={'Cookie': cookie})
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        self.assertEqual(len(result['users']), 8)
        