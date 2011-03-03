# -*- coding: utf-8 -*-
import os, logging, sys
import tornado.httpserver
import tornado.ioloop


__all__ = ["application"]


from sys2do.handlers import *

setting = {
           "static_path": os.path.join(os.path.dirname(__file__), "public"),
           "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
           "login_url": "/login",
           "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
           "debug" : True,
           }

logging.getLogger().setLevel(logging.DEBUG)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/item/.*", ItemHandler),
    (r"/taobao/.*", TaobaoHandler),
    (r"/.*", MainHandler, {"session" : {}}),
], **setting)
