import json
import sys

sys.path.append('TextRank4ZH-master')
sys.path.append('data_util')
sys.path.append('question_generation_1208')
from textrank import *
from preprocess import *
from generate_xml import *
from predict import *

if __name__ == '__main__':
    raw_title_file = 'data/raw_data/raw_title.txt'
    raw_content_file = 'data/raw_data/raw_content.txt'
    pre_content_file = 'data/pre_data/content.txt'

    keyword_file = 'data/summary/keyword.txt'
    keyphrase_file = 'data/summary/keyphrase.txt'
    keysentence_file = 'data/summary/summarys.txt'

    xml_result_file = 'data/xml/result.xml'

    decode_list = train()
    keyword_list, keyphrase_list, keysentenetce_list = textrank(raw_content_file,
                                                                keyword_file=keyword_file,
                                                                keyphrase_file=keyphrase_file,
                                                                keysentence_file=keysentence_file)
    # pre_content_list = transform_content_file(raw_content_file, pre_content_file)
    raw_content_list = []
    raw_title_list = []
    raw_contentlines = open(raw_content_file, "r").readlines()
    for line in raw_contentlines:
        raw_content_list.append(line)
    raw_titlelines = open(raw_title_file, "r").readlines()
    for line in raw_titlelines:
        raw_title_list.append(line)

    generate_xml_by_list(decode_list, keysentenetce_list, raw_content_list, raw_title_list, keyword_list,
                         xml_result_file)
