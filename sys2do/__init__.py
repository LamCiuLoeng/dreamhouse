# -*- coding: utf-8 -*-
import os, logging, sys
import tornado.httpserver
import tornado.ioloop

from sys2do.handlers import *
from sys2do.util.session import TornadoSessionManager


__all__ = ["application"]


setting = {
           "static_path": os.path.join(os.path.dirname(__file__), "public"),
           "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
           "login_url": "/login",
           "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
           "debug" : True,
           "xsrf_cookies": True,
           }

logging.getLogger().setLevel(logging.DEBUG)

application = tornado.web.Application([
    (r"/user/.*", UserHandler),
    (r"/admin/.*", AdminHandler),
    (r"/", RootHandler),
    (r"/.*", RootHandler, {"session" : {}}),
], **setting)


session_setting = {
                   "secret" : "123321",
                   "session_dir" : os.path.join(os.path.dirname(__file__), "session"),
                   }


application.session_manager = TornadoSessionManager(**session_setting)
