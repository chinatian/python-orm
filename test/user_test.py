#!/usr/bin/env python
#-*- coding: utf8 -*-

from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase

import manage
import re

try:
    import simplejson as json
except ImportError:
    import json

class UserTest(AsyncHTTPTestCase):
    def get_app(self):
        return manage.Application()
    def test_signup_post(self):
        response = self.fetch('/user/signup', method="POST", body="name=junfeng009&phone=13811429668")
        user_cookie = re.findall('user=([\w\|]+);', response.headers['Set-Cookie'])[0]
        print user_cookie
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        
        print 'id=%d, password=%s' % (result['user']['id'], result['user']['password'],)
        
        response = self.fetch('/user/signup', method="POST", body="name=junfeng010")
        user_cookie = re.findall('user=([\w\|]+);', response.headers['Set-Cookie'])[0]
        print user_cookie
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        
        cookie = 'user=%s;' % user_cookie
        
        response = self.fetch('/user/signup/phone',
            method="POST",
            body="phone=18610195110",
            headers={'Cookie': cookie})
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        
        print 'id=%d, password=%s' % (result['user']['id'], result['user']['password'],)
        
        response = self.fetch('/user/signup/password',
            method="POST",
            body="password=sa",
            headers={'Cookie': cookie})
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        
