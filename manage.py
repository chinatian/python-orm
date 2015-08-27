#-*- coding: utf8 -*-

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import controllers
import settings
import urls

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, urls.handlers, **settings.OPTIONS)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()