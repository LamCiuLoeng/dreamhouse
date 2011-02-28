# -*- coding: utf-8 -*-
from sqlalchemy import Table, ForeignKey, Column, Float, Boolean
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, synonym

from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin

__all__ = ["Item"]

class Item(DeclarativeBase, SysMixin):

    __tablename__ = 'item'

    id = Column(Integer, autoincrement = True, primary_key = True)

    num_iid = Column(Integer)
    title = Column(Unicode(100))
    type = Column(Unicode(100))
    props_name = Column(Unicode(1000))
    pic_url = Column(Unicode(1000))
    num = Column(Integer)
    valid_thru = Column(Integer)
    list_time = Column(DateTime)
    delist_time = Column(DateTime)
    stuff_status = Column(Unicode(100))
    price = Column(Float)
    post_fee = Column(Float)
    express_fee = Column(Float)
    ems_fee = Column(Float)
    freight_payer = Column(Unicode(100))
    has_invoice = Column(Boolean)
    has_warranty = Column(Boolean)
