# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sys2do.setting import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI, echo = False)
maker = sessionmaker(autoflush = True, autocommit = False)
DBSession = scoped_session(maker)
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata



DBSession.configure(bind = engine)

from auth import User, Group, Permission
from logic import *
