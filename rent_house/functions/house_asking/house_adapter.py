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
            "street":"Thiếu đường, vui lòng nhập nhập thêm muối :))",
            "district":"Thiếu tên quận, vui lòng nhập quận :>",
            "province":"Thiếu tên thành phố, vui lòng nhập thành phố",
            "maxPrice":"Thiếu giá, vui lòng nhập giá trước khi quá muộn :)"
        }

    def can_process(self, statement):
        fb_statement = statement.extra_data
        state=fb_statement['conversation_id'][0]
        if(fb_statement['action']=='__label__house' and (state = 'init' or state='house')):
            return True
        else:
            return False
        # if not fb_statement.has_key('id_adapter'):
        #     rasa_nlu = fb_statement['rasa_nlu']
        #     if self.id_adapter.lower() == rasa_nlu['intent']['name']:
        #         return True
        #     else:
        #         return False
        # else:
        #     return False
        #

    def process(self, statement):
        fb_statement = statement.extra_data
        ss_id=fb_statement['conversation_id'][1]
        print(fb_statement)
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
                statementResponse = Statement(pre_statement)
            else:
                pass
        if pre_statement is None:
            statementResponse = Statement(u"Chào bạn! Tôi có thể giúp gì cho bạn? House")
        statementResponse.confidence = 0.1#rasa_nlu['intent']['confidence']
        # print(statementResponse)
        return statementResponse
