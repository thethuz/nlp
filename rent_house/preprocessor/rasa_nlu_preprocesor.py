import pickle
from pyvi.pyvi import ViTokenizer
import requests
import re
import json
import unidecode
from gensim import corpora, matutils
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
intent_model = dir_path+"/model/intent_model.pkl"
ner_model = dir_path+"/model/ner.pkl"

def __load_dictionary():
    filePath=dir_path+"/intent/dict.txt"
    dictionary = corpora.Dictionary.load_from_text(filePath)
    return dictionary

def get_dense(words):
    dictionary=__load_dictionary()
    vec = dictionary.doc2bow(words)
    dense = list(matutils.corpus2dense([vec], num_terms=len(dictionary)).T[0])
    return dense
stop_words=[]
def get_stop_word():
    f = open(dir_path+"intent/stopwords.txt")
    for row in f:
        stop_words.append(row.strip('0123456789%@$.,=+-!;/()*"&^:#|\n\t\''))
fi = open(intent_model, 'rb')
classify = pickle.load(fi)

fn = open(ner_model, 'rb')
ner = pickle.load(fn)

def extract_intent_entities(chatbot, statement):
    # print(statement)
    # print(type(statement))
    try:
        print(statement.extra_data)
    except:
        print('no extra data')
    try:
        # print(statement.text)
        fb_statement = json.loads(statement.text)
    except:
        fb_statement={'extra_data':statement.text}
    # print(fb_statement)
    # print(type(fb_statement))

    # statement=fb_statement
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
    split_rows = fb_statement['extra_data'].split( )
    for split_row in stop_words:
        if split_row in split_rows:
            split_rows.remove(split_row)
    sentences=ViTokenizer.tokenize(" ".join(str(x) for x in split_rows))
    sentences=sentences.strip('0123456789%@$.,=+-!;/()*"&^:#|\n\t\'?')
    sentences=sentences.replace("<", "")
    sentences=sentences.replace(">", "")
    v1=get_dense(sentences.split( ))
    mtrix=[v1]
    action=classify.predict(mtrix)

    user_message={'action':action[0],'text':fb_statement['extra_data']}
    statement.text = str(fb_statement['extra_data'])
    statement.extra_data = user_message

    statement.confidence=0.9
    print(statement.text)
    return statement
