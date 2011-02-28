# -*- coding: utf-8 -*-
import logging
from urllib import urlencode
from datetime import datetime as dt
import tornado.web
from tornado.httpclient import AsyncHTTPClient

from sys2do.module import *
from MethodDispatcher import MethodDispatcher
from sys2do.util.taobao import TaoBao


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = DBSession.query(Item).all()
        self.render("index.html",items=items)
        
        
class TaobaoHandler(MethodDispatcher):
    def add(self):
        self.render("taobao.html")
    
    @tornado.web.asynchronous
    def save(self,**kw):
        if kw["type"] == "nickname":
            self._by_nickname(kw["value"])

    def _by_nickname(self,nickname):
        page_size = 100
        
        fields1 = ["num_iid","title","nick","pic_url","cid","price","type","delist_time","post_fee"]
        fields2 = ["num_iid","title","nick","type","props_name",
                  "cid","seller_cids","props","pic_url","num","valid_thru","list_time",
                  "delist_time","stuff_status","price","post_fee","express_fee","ems_fee",
                  "has_discount","freight_payer","has_invoice","has_warranty","modified",
                  "approve_status","sell_promise"]
        params1 = dict(
                    method = 'taobao.items.get',
                    nicks = nickname,
                    fields = ",".join(fields1),
                    page_size = page_size
                    )
        
        def _getItemDetail(data):
            info = data["item_get_response"]["item"]
            params = {}
            for f in fields2:
                if f in ["delist_time","list_time","modified","created"] : params[f] = dt.strptime(info[f],"%Y-%m-%d %H:%M:%S")
                else : params[f] = info[f]
            DBSession.add(Item(**params))

        
        def _getLastItemDetail(data):
            _getItemDetail(data)
            DBSession.commit()
            self.render("taobao_result.html")
            
            
        def _getItemList(data):
            logging.info("--------- response start -------------")
            items = data["items_get_response"]["items"]["item"]
#            items = [{"num_iid":"9257172491"}]
            for index,item in enumerate(items):
                p = {
                    "method" : "taobao.item.get",
                    "nick" : nickname,
                    "num_iid" : item["num_iid"],
                    "fields" : ",".join(fields2)
                    }
                
                if index == len(items)-1 : tmp = TaoBao(p,callback=_getLastItemDetail)
                else :tmp = TaoBao(p,callback=_getItemDetail)
                tmp.fetch()
#                params = {}
#                for f in fields : 
#                    if f == "delist_time" : params[f] = dt.strptime(item[f],"%Y-%m-%d %H:%M:%S")
#                    else : params[f] = item[f]
#                DBSession.add(Item(**params))
            
#            DBSession.commit()
#            logging.info("\n".join(ids))
            
        t = TaoBao(params1,callback=_getItemList)
        t.fetch()
            
        
#        http = AsyncHTTPClient()
#        logging.info(urlencode(t._params))
#        http.fetch(t._taobao_url,method="POST",body=urlencode(t._params),callback = self._cb)
        
