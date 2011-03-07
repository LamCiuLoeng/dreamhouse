# -*- coding: utf-8 -*-
import logging, traceback
from datetime import datetime as dt
import tornado.web
from webhelpers.paginate import Page
from sqlalchemy import or_, and_

from sys2do.model import *
from MethodDispatcher import MethodDispatcher
from sys2do.util.taobao import TaoBao


class RootHandler(MethodDispatcher):
    def index(self, **kw):
        items = DBSession.query(Item).all()
        my_page = Page(items, page = int(kw.get("page", 1)), url = lambda page:"%s?page=%d" % (self.request.path, page))
        self.render("index.html", my_page = my_page)




    def login(self, **kw):
        if self.current_user :
            self.redirect("/index")
        else:
            self.render("login.html")

    def login_handler(self, **kw):
        try:
            u = DBSession.query(User).filter(and_(User.user_name == kw.get("username", None), User.password == kw.get("password", None))).one()
            self.session["user_info"] = {
                                         "id" : u.id,
                                         "user_name" : u.user_name,
                                         "display_name" : u.display_name,
                                         "email_address" : u.email_address,
                                         }
            self.session["group_info"] = [str(g) for g in u.groups]
            self.session["permission_info"] = u.permissions
            self.session.save()
            self.set_current_user(u.user_name)
        except:
            self.redirect("/login")
        else:
#            if "admin" in self.session["group_info"]:
#                self.redirect("/admin/index")
#            elif "user" in self.session["group_info"]:
#                self.redirect("/user/index")
#            else:
#                self.redirect("/index")
            self.redirect("/user_dispatch")

    def user_dispatch(self):
        if self.get_current_user() :
            if "admin" in self.session["group_info"]:
                self.redirect("/admin/index")
            elif "user" in self.session["group_info"]:
                self.redirect("/user/index")
            else:
                self.redirect("/index")
        else:
            self.redirect("/index")


    def register(self, **kw):
        self.render("register.html")

    def register_hander(self, **kw):
        username = kw.get("username", None)
        password = kw.get("password", None)
        confirmed_password = kw.get("confirmed_password", None)
        email = kw.get("email", None)

        msg = []
        if not username :
            msg.append("User name could not be blank!")
        elif password != confirmed_password :
            msg.append("Password and confirmed password are not the same!")
        elif not email :
            msg.append("E-mail could not be blank!")
        else:
            try:
                DBSession.query(User).filter(and_(User.active == 0, User.user_name == username)).one()
                msg.append("The user name already exist!")
            except:
                pass

        if msg :
            self.redirect("/login", msg = msg)
        else:
            try:
                u = User(user_name = username, password = password, email_address = email)
                g = DBSession.query(Group).filter(Group.group_name == "user").one()
                g.users.append(u)

                DBSession.add(u)
                DBSession.commit()
            except:
                DBSession.rollback()
                self.redirect("/login")
            else:
                self.redirect("/login")


    def logout(self):
        self.clear_current_user()
        self.redirect("/index")


    def item_detail(self, **kw):
        item = DBSession.query(Item).get(kw["id"])
        self.render("item_detail.html", item = item)


    def item_quick_search(self, **kw):
        result = DBSession.query(Item).filter(Item.title.like("%%%s%%" % kw.get("q", ""))).all()
        my_page = Page(result, page = int(kw.get("page", 1)), url = lambda page:"%s?q=%s&page=%d" % (self.request.path, kw.get("q", ""), page))
        self.render("item_quick_search.html", my_page = my_page)


    def add_to_cart(self, **kw):
        pass

    def view_cart(self, **kw):
        pass

    @tornado.web.authenticated
    def place_order(self, **kw):
        pass

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
        self.session.save()
        self.write("OK")

    def test2(self):
        self.render("test.html")

    def testflash(self):
        self.flash("hello,cl,testing")
        self.write("OK")




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
