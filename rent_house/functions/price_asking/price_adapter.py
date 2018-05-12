# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from django.conf import settings as gs_settings
from pymongo import MongoClient
from rent_house.functions import JhConnector
import json
client = MongoClient('mongodb://localhost:27017/')
db=client.airbnb
prices_col=db.prices

class PriceAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(PriceAdapter, self).__init__(**kwargs)
        self.jhConnector = JhConnector(gs_settings.HOST_API)
        self.id_adapter = 'PRICE'
        self.pattern={
        "ward":"Thiếu đường, vui lòng nhập nhập thêm muối :))",
        "district":"Thiếu tên quận, vui lòng nhập quận :>",
        "province":"Thiếu tên thành phố, vui lòng nhập thành phố",
        }
        self.session={}

    def can_process(self, statement):
        fb_statement = statement.extra_data
        state=fb_statement['conversation_id'][0]
        print(state)
        if((fb_statement['action']=='__label__price' and state == 'init') or state == 'price'):
            return True
        else:
            return False

    def process(self, statement):
        fb_statement = statement.extra_data
        ss_id=fb_statement['conversation_id'][1]
        print(fb_statement)
        ner=fb_statement['ner']
        try:
            self.session[ss_id]
        except:
            self.session[ss_id]={'ward':None,'district':None,'province':None}
        for key,value in ner.items():
            if key in self.session[ss_id]:
                self.session[ss_id][key]=value
        print("\n self session is "+str(self.session))
        pre_statement=None
        # for key,value in self.session[ss_id].items():
        #     if value is None:
        #         pre_statement=self.pattern[key]
        if self.session[ss_id]['province'] is None:
            pre_statement=self.pattern['province']

        if pre_statement is None:
            print('statement is null')
            statement.extra_data['conversation_id'][0]='done'
            text=self.findPrice(self.session[ss_id])
            # statement.text=u"Chào bạn! Tôi có thể giúp gì cho bạn? Price"
            self.session[ss_id]={'ward':None,'district':None,'province':None}
            statement.text=text
        else:
            print('statement is not null')
            statement.text=pre_statement
            statement.extra_data['conversation_id'][0]='price'
        return statement
    def findAddressByAddr(self, addr, typeAdr=None):
        url = '/api/analyst/getfromaddr?addr=' + addr
        if typeAdr is not None:
            url += '&type=' + typeAdr
        return json.loads(self.jhConnector.get(url).content.decode("utf-8"))[0]
    def findPrice(self,entity):
        condition=u''
        if(entity['ward'] is not None):
            condition+=str(entity['ward'])+' '
        if(entity['district'] is not None):
            condition+=str(entity['district'])+' '
        condition+=str(entity['province'])
        # condition1=self.findAddressByAddr(condition)
        # print(condition1)
        price = prices_col.find_one({'addr':condition.replace('_',' ')})
        print({'addr':condition.replace('_',' ')})
        # print(price)
        if price is None:
            return 'Chúng tôi không có thông tin về địa điểm này :('
        else:
            txt='Giá trung bình của '+condition.replace('_',' ')+' là '+str(round(price['price'],3)*1000000)+' đồng'
            return txt
        # pass
