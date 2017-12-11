# -*- encoding:utf-8 -*-
from __future__ import print_function

import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def textrank(raw_content_file, keyword_file='data/summary/keyword.txt',
             keyphrase_file='data/summary/keyphrase.txt', keysentence_file='data/summary/summarys.txt'):
    s_f = open(raw_content_file, 'r')
    keyword_file = open(keyword_file, 'w')
    keyphrase_file = open(keyphrase_file, 'w')
    keysentence_file = open(keysentence_file, 'w')
    lines = s_f.readlines()  # 读取全部内容
    keyword_list = []
    keyphrase_list = []
    keysentence_list = []
    for text in lines:
        # text = codecs.open('../test/doc/content1.txt', 'r', 'utf-8').read()
        tr4w = TextRank4Keyword()

        tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

        keyword = ""
        keyphrase = ""
        keysentence = ""

        print('关键词：')
        for item in tr4w.get_keywords(10, word_min_len=1):
            keyword += item.word + " "
            # print(item.word, item.weight)
        keyword_file.write(keyword + "\n")
        keyword_list.append(keyword)

        print()
        print('关键短语：')

        for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
            keyphrase += phrase + " "
        keyphrase_file.write(keyphrase + "\n")
        keyphrase_list.append(keyphrase)
        # print(phrase)

        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source='all_filters')

        print()
        print('摘要：')
        for item in tr4s.get_key_sentences(num=5):
            keysentence += item.sentence
            if len(keysentence) > 100:
                break
        keysentence_file.write(keysentence + "\n")
        keysentence_list.append(keysentence)

    return keyword_list, keyphrase_list, keysentence_list
        # print(item.index, item.weight, item.sentence)
