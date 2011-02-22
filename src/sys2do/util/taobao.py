# -*- coding: utf-8 -*-
import time
import hmac
import urllib
import urllib2
import json

class TaoBao(object):

    def __init__(self, dict_param = {}, format = 'json'):
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
        self._sign()
        self._fetch()

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

    def _fetch(self):
        try:
            self.rsp = urllib2.urlopen(self._taobao_url, urllib.urlencode(self._params)).read()
        except:
            self.rsp = None

    def get_data(self):
        if self.rsp:
            if 'json' == self._params['format']:
                    rsp = json.loads(self.rsp)
                    if 'error_response' in rsp:
                        return None
                    else:
                        return rsp
            else:
                return self.rsp
        else:
            return None




if __name__ == '__main__':
    """
    data = dict(
                    method='taobao.user.get',
                    fields='user_id,nick,sex,buyer_credit,seller_credit,location.country,created,last_visit,location.zip,birthday,type,has_more_pic,item_img_num,item_img_size,prop_img_num,prop_img_size,auto_repost,promoted_type,status,alipay_bind,consumer_protection',
                    nick='97乐淘易购网',
                    )
    taobao = TaoBao()
    taobao.setParams(data)
    rs = taobao.fetch()
    print rs
    print (u'97\u4e50\u6dd8\u6613\u8d2d\u7f51').encode('utf-8')
    

    data = dict(method='taobao.koubei.store.search', city_id='359')
    taobao = TaoBao(data)
    #taobao = TaoBao()
    rs = taobao.get_data()
    print rs
    """
    params = dict(
                    method = 'taobao.taobaoke.items.convert',
                    fields = 'click_url',
                    num_iids = '4700935763,7486981099,7641176939,3572375175,7512138535,5127449911,4116154837,5250482751,3606568529,7512939381,7772500999,5961280639,7760300533,4782615585,7798413431,4857602079,7524467577,7454547337',
                    nick = 'xieren58'
                    )
    taobao = TaoBao(params)
    rs = taobao._fetch()
    #rs = taobao.get_data()
    print rs
