# -*- coding: utf-8 -*-
import logging, traceback
from urllib import urlencode
from datetime import datetime as dt
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from webhelpers.paginate import Page

from sys2do.model import *
from MethodDispatcher import MethodDispatcher
from sys2do.util.taobao import TaoBao
from sys2do import setting


class MainHandler(MethodDispatcher):
    def index(self, **kw):
        items = DBSession.query(Item).all()
#        import pdb
#        pdb.set_trace()
        my_page = Page(items, page = int(kw.get("page", 1)), url = lambda page:"%s?page=%d" % (self.request.uri, page))
#        logging.info(my_page)
        self.render("index.html", my_page = my_page)


#    def testip(self):
#        if not self.request.remote_ip: self.finish()
#        def _call(response):
#            logging.info(response.body)
#            self.finish()
#
#        http = AsyncHTTPClient()
#        http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=%s" % self.request.remote_ip, callback = _call)

    def test1(self, **kw):
        self.session["aa"] = kw["aa"]
        self.write("OK")

    def test2(self):
        self.write(self.session["aa"])

class ItemHandler(MethodDispatcher):
    def detail(self, **kw):
        item = DBSession.query(Item).get(kw["id"])
        self.render("item_detail.html", item = item)

class TaobaoHandler(MethodDispatcher):
    def add(self):
        self.render("taobao.html")

    @tornado.web.asynchronous
    def save(self, **kw):
        if kw["type"] == "nickname":
            self._by_nickname(kw["value"], kw["page"])

    def _by_nickname(self, nickname, page):
        page_size = 50

        fields1 = ["num_iid", "title", "nick", "pic_url", "cid", "price", "type", "delist_time", "post_fee"]
        fields2 = ["num_iid", "title", "nick", "type", "props_name",
                  "cid", "seller_cids", "props", "pic_url", "num", "valid_thru", "list_time",
                  "delist_time", "stuff_status", "price", "post_fee", "express_fee", "ems_fee",
                  "has_discount", "freight_payer", "has_invoice", "has_warranty", "modified",
                  "approve_status", "sell_promise", "desc"]
        params1 = dict(
                    method = 'taobao.items.get',
                    nicks = nickname,
                    fields = ",".join(fields1),
                    page_size = page_size,
                    page_no = page
                    )

        def _getItemDetail(data):
            try:
                info = data["item_get_response"]["item"]
                try:
                    t = DBSession.query(Item).filter(Item.num_iid == info["num_iid"]).one()
                    for f in fields2:
                        if f in ["delist_time", "list_time", "modified", "created"] :
                            setattr(t, f, dt.strptime(info[f], "%Y-%m-%d %H:%M:%S"))
                        else:
                            setattr(t, f, info[f])
                except:
                    params = {}
                    for f in fields2:
                        if f in ["delist_time", "list_time", "modified", "created"] : params[f] = dt.strptime(info[f], "%Y-%m-%d %H:%M:%S")
                        else : params[f] = info[f]
                    DBSession.add(Item(**params))
            except:
                logging.error(traceback.print_exc())

        def _getLastItemDetail(data):
            _getItemDetail(data)
            DBSession.commit()
            self.render("taobao_result.html")


        def _getItemList(data):
            logging.info("--------- response start -------------")
            items = data["items_get_response"]["items"]["item"]
#            items = [{"num_iid":"9257172491"}]
            for index, item in enumerate(items):
                p = {
                    "method" : "taobao.item.get",
                    "nick" : nickname,
                    "num_iid" : item["num_iid"],
                    "fields" : ",".join(fields2)
                    }

                if index == len(items) - 1 : tmp = TaoBao(p, callback = _getLastItemDetail)
                else :tmp = TaoBao(p, callback = _getItemDetail)
                tmp.fetch()
#                params = {}
#                for f in fields : 
#                    if f == "delist_time" : params[f] = dt.strptime(item[f],"%Y-%m-%d %H:%M:%S")
#                    else : params[f] = item[f]
#                DBSession.add(Item(**params))

#            DBSession.commit()
#            logging.info("\n".join(ids))

        t = TaoBao(params1, callback = _getItemList)
        t.fetch()
