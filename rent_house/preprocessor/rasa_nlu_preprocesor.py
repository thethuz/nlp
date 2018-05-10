import pickle
from pyvi.pyvi import ViPosTagger,ViTokenizer
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

def tupToList(tup):
    list1=[]
    for item in tup[0]:
        index=tup[0].index(item)
        tup_=(item,tup[1][index],'0')
        list1.append(tup_)
    return list1
def getMatrix(data):
    matrix=[]
    vector=[]
    line=0
    for dt in data:
        if len(dt)>1:
            dt = dt[:-1]
            l1=dt.split(" ")
            t1=(l1[0],l1[1],l1[2])
            vector.append(t1)
        else:
            matrix.append(vector)
            vector=[]
    matrix.append(vector)
    # print (len(matrix))
    return matrix
def make_data_train(row):
    data_train=[]
    # for row in data:
    post_tup=ViPosTagger.postagging(ViTokenizer.tokenize(row))
    post_list=tupToList(post_tup)
    data_train.append(post_list)
    return data_train
def writeListFile(data):
    str_out=[]
    for item in data:
        for tup in item:
            str_out.append(tup[0]+" "+tup[1]+" "+tup[2]+"\n")
    return str_out
def ner_exact(test_list_sentence):
    test_sentence=make_data_train(test_list_sentence)
    data_test=writeListFile(test_sentence)
    matrix_test_sentence=getMatrix(data_test)
    X_matrix_test_sentence = [sent2features(s) for s in matrix_test_sentence]
    y_pred = ner.predict(X_matrix_test_sentence)
    # print(test_list_sentence.split())
    # print(y_pred)
    entity_dict={}
    l1=test_list_sentence.split()
    # print(l1)
    # print(y_pred)
    for l000,l001 in zip(l1,y_pred[0]):
        # print(l000, l001)
        if l001!='0':
            # i={l001:l000}
            entity_dict[l001]=l000
    return entity_dict

def extract_intent_entities(chatbot, statement):
    print('statement'+str(statement))
    # try:
    #     print(statement.extra_data)
    # except:
    #     print('no extra data')
    try:
        fb_statement = json.loads(statement.text)
    except:
        fb_statement={'extra_data':statement.text}
    # print(fb_statement)
    # print("\n\n")
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
    split_rows = fb_statement['text'].split( )
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
    # print('ner:')
    ner_dict=ner_exact(sentences)
    # print(ner_dict)
    # print(sentences)
    user_message={'action':action[0],'text':fb_statement['text'],'ner':ner_dict,'conversation_id':fb_statement['session']}
    statement.text = str(fb_statement['text'])
    statement.extra_data = user_message

    statement.confidence=0.9
    # print("statement.text: "+statement.text)
    # print("statement.extra_data: "+str(statement.extra_data))
    return statement

#
#
#
def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]
