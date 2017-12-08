#-*-coding:utf-8-*-
'''
根据一个给定的XML Schema，使用DOM树的形式从空白文件生成一个XML。
'''
from xml.dom.minidom import Document
import uuid
import time
import re

def geneterate_xml(topictile_file, abstract_file,raw_content_file, raw_title_file):
    doc = Document()  #创建DOM文档对象
    # for i in range(0,3):
    DOCUMENT = doc.createElement('TopicList') #创建根元素
    # DOCUMENT.setAttribute('content_method',"full")#设置命名空间
    #DOCUMENT.setAttribute('xsi:noNamespaceSchemaLocation','DOCUMENT.xsd')#引用本地XML Schema
    doc.appendChild(DOCUMENT)
    ############item:Python处理XML之Minidom################
    #item.setAttribute('genre','XML')
    topictitle = []
    abstract = []
    raw_content = []
    raw_title = []

    topiclines = open(topictile_file, "r").readlines()
    for line in topiclines:
        topictitle.append(line)

    abstractlines = open(abstract_file, "r").readlines()
    for line in abstractlines:
        abstract.append(line)

    raw_contentlines = open(raw_content_file, "r").readlines()
    for line in raw_contentlines:
        raw_content.append(line)

    raw_titlelines = open(raw_title_file, "r").readlines()
    for line in raw_titlelines:
        raw_title.append(line)


    # print len(topictitle)
    # print topictitle[0]
    #
    # print len(abstract)
    # print abstract[0]
    #
    #
    # print len(raw_content)
    # print raw_content[0]
    #
    # print len(raw_title)
    # print raw_title[0]

    for i in range(50,100):
        Topic = doc.createElement('Topic')
        # print str(uuid.uuid1())
        uuids = ''.join(str(uuid.uuid1()).split('-'))
        Topic.setAttribute('id', uuids)
        DOCUMENT.appendChild(Topic)

        TopicClass = doc.createElement('TopicClass')
        TopicClass_text = doc.createTextNode('创新评估类') #元素内容写入
        TopicClass.appendChild(TopicClass_text)
        Topic.appendChild(TopicClass)

        TopicTitle = doc.createElement('TopicTitle')
        #todo:
        TopicTitle_text = doc.createTextNode(topictitle[i].strip()+"?")  # 元素内容写入
        TopicTitle.appendChild(TopicTitle_text)
        Topic.appendChild(TopicTitle)

        Abstract_ = doc.createElement('Abstract')
        #todo:
        Abstract_text = doc.createTextNode(abstract[i].strip())
        Abstract_.appendChild(Abstract_text)
        Topic.appendChild(Abstract_)

        CreateTime = doc.createElement('CreateTime')
        CreateTime_text = doc.createTextNode(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))  # 元素内容写入
        CreateTime.appendChild(CreateTime_text)
        Topic.appendChild(CreateTime)

        ReferenceInfoList = doc.createElement('ReferenceInfoList')
        Topic.appendChild(ReferenceInfoList)

        Reference = doc.createElement('Reference')
        Reference.setAttribute('id','1')
        #todo:
        str_combind = raw_title[i] + raw_content[i]
        lines = re.split("！|。|？", str_combind)
        reference_str = ""
        if i ==5:
            print len(lines)
        for line in lines:
            reference_str+=line
            if len(reference_str)>200:
                break


        Reference_text =  doc.createTextNode(reference_str)
        Reference.appendChild(Reference_text)
        ReferenceInfoList.appendChild(Reference)

        keyword = doc.createElement('keyword')
        keyword.setAttribute('id','1')
        keyword_text = doc.createTextNode('人工智能')
        keyword.appendChild(keyword_text)
        ReferenceInfoList.appendChild(keyword)

        ########### 将DOM对象doc写入文件
        f = open('../data/xml/topic_news_50_100.xml','w')
        #f.write(doc.toprettyxml(indent = '\t', newl = '\n', encoding = 'utf-8'))
        doc.writexml(f,indent = '\t',newl = '\n', addindent = '\t',encoding='utf-8')
        # line = f.readline()
    f.close()
geneterate_xml('../data/decode.txt','../data/summary/summarys.txt','../data/raw_content.txt', '../data/raw_title.txt')

