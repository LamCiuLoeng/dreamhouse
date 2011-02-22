# -*- coding: utf-8 -*-
import os, logging, sys
import tornado.httpserver
import tornado.ioloop

from sys2do.handlers import *

setting = {
           "static_path": os.path.join(os.path.dirname(__file__), "public"),
           "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
           "login_url": "/login",
           "template_path" : "templates",
           "debug" : True,
           }

logging.getLogger().setLevel(logging.DEBUG)

application = tornado.web.Application([
    (r"/", MainHandler),
], **setting)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    logging.info("starting torando web server")
