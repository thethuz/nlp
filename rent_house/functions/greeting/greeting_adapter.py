# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class GreetingAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(GreetingAdapter, self).__init__(**kwargs)
        self.id_adapter = 'GREETING'

    def can_process(self, statement):
        fb_statement = statement.extra_data
        # print(type(fb_statement))
        # print(fb_statement['action'])
        return False
        # if(fb_statement['action']=='__label__greeting'):
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
        # fb_statement['confidence']=0.9
        # rasa_nlu = fb_statement['rasa_nlu']
        statementResponse = Statement(u"Chào bạn! Tôi có thể giúp gì cho bạn? Greeting")

        statementResponse.confidence = 0.1#rasa_nlu['intent']['confidence']
        # print('________________')
        # print(statementResponse)
        # print('________________')
        return statementResponse
