# -*- coding: utf-8 -*-
import os, logging, sys
import tornado.httpserver
import tornado.ioloop

from sys2do import application


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    logging.info("starting torando web server")
    logging.info(os.path.dirname(__file__))
#    tornado.ioloop.IOLoop.instance().start()
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
