# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from rent_house.functions import JhConnector
from django.conf import settings as gs_settings
import json
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db=client.airbnb
homes=db.airbnb_homes
class HouseAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(HouseAdapter, self).__init__(**kwargs)
        self.id_adapter = 'HOUSE'
        self.session={}
        self.jhConnector = JhConnector(gs_settings.HOST_API)
        self.pattern={
        "province":"Thiếu tên thành phố, vui lòng nhập thành phố",
        "district":"Thiếu tên quận, vui lòng nhập quận :>",
        "ward":"Thiếu phường, vui lòng nhập nhập phường :))",
        "maxPrice":"Thiếu giá, vui lòng nhập giá trước khi quá muộn :)",
        }

    def can_process(self, statement):
        fb_statement = statement.extra_data
        state=fb_statement['conversation_id'][0]
        print('\nstate: '+state)
        if((fb_statement['action']=='__label__house' and state == 'init') or state == 'house'):
            return True
        else:
            return False


    def process(self, statement):
        fb_statement = statement.extra_data
        ss_id=fb_statement['conversation_id'][1]

        ner=fb_statement['ner']
        try:
            self.session[ss_id]
        except:
            self.session[ss_id]={'ward':None,'district':None,'province':None,'maxPrice':None}
        for key,value in ner.items():
            if key in self.session[ss_id]:
                self.session[ss_id][key]=value
        print("\n self session is "+str(self.session))
        pre_statement=None
        for key,value in self.session[ss_id].items():
            if value is None:
                pre_statement=self.pattern[key]
                break

        if pre_statement is None:
            statement.extra_data['conversation_id'][0]='done'
            text=self.findHouse(self.session[ss_id])
            self.session[ss_id]={'ward':None,'district':None,'province':None,'maxPrice':None}
            statement.text=text
            pass
        else:
            statement.text=pre_statement
            statement.extra_data['conversation_id'][0]='house'
        print('\n---statement.text: '+statement.text)

        return statement

    def findAddressByAddr(self, addr, typeAdr=None):
        url = '/api/analyst/getfromaddr?addr=' + addr
        if typeAdr is not None:
            url += '&type=' + typeAdr
        return json.loads(self.jhConnector.get(url).content.decode("utf-8"))[0]
    def findHouse(self,entity):
        homes_result=homes.find({"details.ward":entity['ward'].replace('_',' '),
        "details.price":{"$lt":float(entity['maxPrice'])}
        ,"details.district":entity['district'].replace('_',' '),
        "details.province":entity['province'].replace('_',' ')},
        {"details.name":1,"details.sectioned_description.description":1,
        "details.address":1,"details.price":1,"details.amenities.name":1,"details.pictures":1}).limit(5)
        txt=u''
        list1=[]
        print(homes_result)
        for home in homes_result:
            txt+='Tên: '+str(home['details']['name'])+'\n'
            txt+='Địa chỉ: '+str(home['details']['address'])+'\n'
            des_list=home['details']['sectioned_description']['description'].split('.')[:2]
            txt+='Mô tả: '+'.'.join(des_list)+'\n'

            amenities=home['details']['amenities']
            amen_txt=u''
            for a in amenities:
                amen_txt+=a['name']
            txt = txt[:-1]
            txt+=',\n'
            txt+='price:'+str(home['details']['price'])+'\n'
            txt+='url:"www.airbnb.com/rooms/'+str(home['_id'])+'\n'
            txt+='picture:'+str(home['details']['pictures'])+'\n'
            print(txt)
            item={}
            item[u'Tên']=home['details']['name']
            item[u'Địa chỉ']=home['details']['address']
            item[u'Mô tả']='.'.join(des_list)
            item[u'Tiện ích']=amen_txt
            item[u'Giá']=str(home['details']['price']*1000000)+'đồng'
            item[u'Ảnh']=home['details']['pictures']
            item[u'url']='airbnb.com/rooms/'+str(home['_id'])
            list1.append(item)
        return str(list1)
