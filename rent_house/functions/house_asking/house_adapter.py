# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class HouseAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(HouseAdapter, self).__init__(**kwargs)
        self.id_adapter = 'HOUSE'
        self.session={}
        self.pattern={
        "province":"Thiếu tên thành phố, vui lòng nhập thành phố",
        "district":"Thiếu tên quận, vui lòng nhập quận :>",
        "street":"Thiếu đường, vui lòng nhập nhập thêm muối :))",
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
        # print(fb_statement)
        ner=fb_statement['ner']
        try:
            self.session[ss_id]
        except:
            self.session[ss_id]={'street':None,'district':None,'province':None,'maxPrice':None}
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
            statement.text=u"Chào bạn! Tôi có thể giúp gì cho bạn? House"
            pass
        else:
            statement.text=pre_statement
            statement.extra_data['conversation_id'][0]='house'
        print('\n---statement.text: '+statement.text)
        # print(statement.extra_data)

        return statement
