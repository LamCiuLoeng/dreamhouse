# -*- coding: utf-8 -*-
import os, sys

__all__ = ["SQLALCHEMY_DATABASE_URI"]

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(os.path.dirname(__file__), "dreamhouse.db"))

if __name__ == "__main__":
    print "\n".join(sys.path)
