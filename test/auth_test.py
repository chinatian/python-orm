#!/usr/bin/env python
#-*- coding: utf8 -*-

from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase

import manage

try:
    import simplejson as json
except ImportError:
    import json

class AuthTest(AsyncHTTPTestCase):
    def get_app(self):
        return manage.Application()
    def test_login_get(self):
        response = self.fetch('/auth/login')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'get Login')
    def test_login_post(self):
        response = self.fetch('/auth/login', method="POST", body="username=13811429668&password=123456")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        print response.body
        
        response = self.fetch('/auth/login', method="POST", body="username=18610195110&password=sa")
        self.assertEqual(response.code, 200)
        result = json.loads(response.body)
        self.assertTrue(result['success'])
        print response.body
