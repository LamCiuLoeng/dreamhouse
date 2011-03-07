# -*- coding: utf-8 -*-
import os

__all__ = ["SQLALCHEMY_DATABASE_URI"]

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(os.path.dirname(__file__), "dreamhouse.db"))
