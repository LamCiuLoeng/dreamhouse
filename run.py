# -*- coding: utf-8 -*-
import os, logging, sys
import tornado.httpserver
import tornado.ioloop

from sys2do import application

def start_server():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    logging.info("starting torando web server")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    start_server()
