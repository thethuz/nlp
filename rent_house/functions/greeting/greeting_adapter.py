# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import random

class GreetingAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(GreetingAdapter, self).__init__(**kwargs)
        self.id_adapter = 'GREETING'
        self.pattern = [u"Chào bạn, chúng tôi có thể giúp gì cho bạn",
                        u"Hihi :))",
                        u"Mình không hiểu gì cả :v",
                        u":)",
                        u"Cảm ơn bạn đã sử dụng.",
                        u"Bạn thật là vui tính quá đi"]

    def can_process(self, statement):
        fb_statement = statement.extra_data
        state = fb_statement['conversation_id'][0]
        if(fb_statement['action'] == '__label__greeting' and (state='init')):
            return True
        else:
            return False

    def process(self, statement):
        fb_statement = statement.extra_data
        # fb_statement['confidence']=0.9
        # rasa_nlu = fb_statement['rasa_nlu']

        statementResponse = Statement(random.choice(pattern))

        # statementResponse.confidence=0.1  # rasa_nlu['intent']['confidence']
        # print('________________')
        # print(statementResponse)
        # print('________________')
        return statementResponse
