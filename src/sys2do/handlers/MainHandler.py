# -*- coding: utf-8 -*-
import logging
import tornado.web

from sys2do.util.taobao import TaoBao

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://friendfeed-api.com/v2/feed/bret", callback = self.on_response)
        logging.info("index bb")
        self.render("index.html")

    def on_response(self, response):
        if response.error: raise tornado.web.HTTPError(500)
        json = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries "
                   "from the FriendFeed API")
        self.finish()
