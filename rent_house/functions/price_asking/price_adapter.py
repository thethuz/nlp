# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class PriceAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(PriceAdapter, self).__init__(**kwargs)
        self.id_adapter = 'PRICE'

    def can_process(self, statement):
        fb_statement = statement.extra_data
        # print('fb_statement: '+str(fb_statement))
        return False
        # if(fb_statement['action']=='__label__greeting'):
        #     return True
        # else:
        #     return False

    def process(self, statement):
        fb_statement = statement.extra_data
        # rasa_nlu = fb_statement['rasa_nlu']
        # fb_statement['confidence']=0.2
        statementResponse = Statement(u"Chào bạn! Tôi có thể giúp gì cho bạn? Price")
        statementResponse.confidence = 0.1#rasa_nlu['intent']['confidence']
        # print(statementResponse)
        return statementResponse
