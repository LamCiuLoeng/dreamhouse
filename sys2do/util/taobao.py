# -*- coding: utf-8 -*-
import time
import hmac
import urllib
import urllib2
import json
import traceback
import logging

from tornado.httpclient import AsyncHTTPClient
from common import makeException

class TaoBao(object):

    def __init__(self, dict_param = {}, format = 'json', callback = None):
        self._sercet_code = '2ea6266fb900a0f8640f4a394f837cab'
        self._taobao_url = 'http://gw.api.taobao.com/router/rest'

        self._params = dict(
                             api_key = '12019856',
                             v = '2.0',
                             sign_method = 'hmac',
                             format = 'json',
                             )
        self.set_params(dict_param)
        self.set_format(format)
        self._callback = callback
        self.rsp = None
        self._sign()


    def set_params(self, dict_param):
        if dict_param and isinstance(dict_param, dict):
            self._params.update(dict_param)

    def set_format(self, format):
        if format.lower() in ('json', 'xml'):
            self._params['format'] = format.lower()

    def _sign(self):
        self._params['timestamp'] = time.strftime('%Y-%m-%d %X', time.localtime())
        self._params['sign'] = hmac.new(self._sercet_code,
                                        ''.join(["%s%s" % (k, v) for k, v in sorted(self._params.items())])).hexdigest().upper()

    def fetch(self):
        http = AsyncHTTPClient()
        http.fetch(self._taobao_url, method = "POST", body = urllib.urlencode(self._params), callback = self.handleResponse)


    def handleResponse(self, response):
        self.rsp = response.body
#        f = file("e:/taobao.txt","ab")
#        f.write(self.rsp)
#        f.close()
#        logging.info(response.body)
        data = self.get_data()
        self._callback(data)

#    def _fetch(self):
#        try:
#            self.rsp = urllib2.urlopen(self._taobao_url, urllib.urlencode(self._params)).read()
#        except:
#            traceback.print_exc()
#            self.rsp = None

    def get_data(self):
        if self.rsp:
            if 'json' == self._params['format']:
                    rsp = json.loads(self.rsp, strict = False)
                    if 'error_response' in rsp:
                        raise makeException(rsp["error_response"]["msg"])
                        return None
                    else:
                        return rsp
            else:
                return self.rsp
        else:
            return None




if __name__ == '__main__':
    params = dict(
                    method = 'taobao.items.search',
                    fields = 'num_iid,title,nick,pic_url,cid,price,type,delist_time,post_fee,score,volume',
                    q = "ps 3",
#                    num_iids = '4700935763,7486981099,7641176939,3572375175,7512138535,5127449911,4116154837,5250482751,3606568529,7512939381,7772500999,5961280639,7760300533,4782615585,7798413431,4857602079,7524467577,7454547337',
#                    nick = 'xieren58'
                    )
    taobao = TaoBao(params)
    taobao._fetch()
    rs = taobao.get_data()
    print rs
    for item in rs["items_search_response"]["item_search"]["items"]["item"]:
        print item
#        print item["title"],item["num_iid"],item["detail_url"],item["pic_url"]

    print "-------------- finish ------------------"
