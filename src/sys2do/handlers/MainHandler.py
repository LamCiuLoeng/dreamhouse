# -*- coding: utf-8 -*-
import logging
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("index bb")
        self.render("index.html")
