#!/usr/bin/env python
#-*- coding: utf8 -*-

import unittest

TEST_MODULES = [
    #'test.user_test',
    'test.auth_test',
    'test.friend_test'
]

def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    import tornado.testing
    tornado.testing.main()
