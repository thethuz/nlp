import pickle
from pyvi.pyvi import ViTokenizer
import requests
import re
import json
import unidecode

intent_model = "./model/intent_model.pkl"
ner_model = "./model/ner.pkl"

def extract_intent_entities(chatbot, statement):
    print(statement)
    print(type(statement))
    try:
        fb_statement = json.loads(statement.text)
    except:
        fb_statement={'extra_data':'hello'}
    statement=fb_statement
    """
    process(self, statement) -> response
    :param
        fb_statement = {
            'fb_id': u"id user facebook",
            'session': u"system session",
            'message': u"message of user",
            'id_adapter'
        }
    :return
            response: doi tuong cua lop Statement
	Xu ly nlu tra ve intent va entities
    """
    # Xu ly xau tieng viet khong dau

    # print rasa_nlu['intent']
    # extraDataService = extractByService(user_message)
    # print extraDataService

    # print json.dumps(rasa_nlu, ensure_ascii=False, indent=4)

    return statement
