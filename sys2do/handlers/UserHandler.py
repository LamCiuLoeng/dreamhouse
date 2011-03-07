# -*- coding: utf-8 -*-
import logging, traceback
from datetime import datetime as dt

import tornado.web

from webhelpers.paginate import Page
from sqlalchemy import or_, and_

from sys2do.model import *
from MethodDispatcher import MethodDispatcher


class UserHandler(MethodDispatcher):
    def index(self, **kw):
        self.render("user/index.html")


    def buyer(self, **kw):
        self.render("user/buyer.html")

    def seller(self, **kw):
        self.render("user/seller.html")
