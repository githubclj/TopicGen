#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
# from textrank4zh
from textrank4zh import TextRank4Keyword, TextRank4Sentence

s_f = open('../../data/raw_content.txt', 'r')
keyword_file = open('../../data/summary/keyword.txt', 'w')
keyphrase_file = open('../../data/summary/keyphrase.txt', 'w')
keysentence_file = open('../../data/summary/summarys.txt', 'w')
lines = s_f.readlines()  # 读取全部内容
for text in lines:
    # text = codecs.open('../test/doc/content1.txt', 'r', 'utf-8').read()
    tr4w = TextRank4Keyword()

    tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

    keyword = ""
    keyphrase = ""
    keysentence = ""

    print( '关键词：' )
    for item in tr4w.get_keywords(10, word_min_len=1):
        keyword+=item.word+" "
        # print(item.word, item.weight)
    keyword_file.write(keyword + "\n")

    print()
    print( '关键短语：' )

    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
        keyphrase+=phrase+" "
    keyphrase_file.write(keyphrase+"\n")
        # print(phrase)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    print()
    print( '摘要：' )
    for item in tr4s.get_key_sentences(num=5):
        keysentence+=item.sentence
        if len(keysentence)>100:
            break
    keysentence_file.write(keysentence+"\n")
        # print(item.index, item.weight, item.sentence)