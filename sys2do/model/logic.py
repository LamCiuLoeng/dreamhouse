# -*- coding: utf-8 -*-
from sqlalchemy import ForeignKey, Column, Float, Boolean
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, backref

from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin

__all__ = ["Catetory", "Item"]


class Catetory(DeclarativeBase, SysMixin):
    __tablename__ = 'category'

    id = Column(Integer, autoincrement = True, primary_key = True)


class Item(DeclarativeBase, SysMixin):

    __tablename__ = 'item'

    id = Column(Integer, autoincrement = True, primary_key = True)

    detail_url = Column(Unicode(200))
    num_iid = Column(Integer)
    title = Column(Unicode(100))
    nick = Column(Unicode(100))
    type = Column(Unicode(100))
    props_name = Column(Unicode(1000))
    promoted_service = Column(Unicode(10))
    cid = Column(Integer)
    seller_cids = Column(Unicode(100))
    props = Column(Unicode(100))
    desc = Column(Unicode(5000))
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
    has_discount = Column(Boolean)
    freight_payer = Column(Unicode(100))
    has_invoice = Column(Boolean)
    has_warranty = Column(Boolean)
    modified = Column(DateTime)
    approve_status = Column(Unicode(100))
    product_id = Column(Integer)
    item_imgs = Column(Unicode(100))
    prop_imgs = Column(Unicode(100))
    sell_promise = Column(Boolean)


class OrderHeader(DeclarativeBase, SysMixin):

    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)


class OrderDetail(DeclarativeBase, SysMixin):

    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("details", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderDetail.header_id, OrderDetail.active == 0)")
