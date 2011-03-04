# -*- coding: utf-8 -*-
import logging, traceback
from urllib import urlencode
from datetime import datetime as dt
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from webhelpers.paginate import Page
from sqlalchemy import or_, and_

from sys2do.model import *
from MethodDispatcher import MethodDispatcher
from sys2do.util.taobao import TaoBao
from sys2do import setting


class UserHandler(MethodDispatcher):
    def index(self, **kw):
        self.render("user/index.html")
