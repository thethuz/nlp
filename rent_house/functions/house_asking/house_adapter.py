# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class HouseAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(HouseAdapter, self).__init__(**kwargs)
        self.id_adapter = 'HOUSE'
        self.session={}

    def can_process(self, statement):
        fb_statement = statement.extra_data
        print(fb_statement)
        return True
        # if(fb_statement['action']=='__label__house'):
        #     return True
        # else:
        #     return False
        # if not fb_statement.has_key('id_adapter'):
        #     rasa_nlu = fb_statement['rasa_nlu']
        #     if self.id_adapter.lower() == rasa_nlu['intent']['name']:
        #         return True
        #     else:
        #         return False
        # else:
        #     return False

    def process(self, statement):
        fb_statement = statement.extra_data
        ss_id=fb_statement['conversation_id']
        try:
            self.session[ss_id]+=1
        except:
            self.session[ss_id]=1
        print(self.session)
        statementResponse = Statement(u"Chào bạn! Tôi có thể giúp gì cho bạn? House")
        statementResponse.confidence = 0.1#rasa_nlu['intent']['confidence']
        # print(statementResponse)
        return statementResponse
