#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re


def preprocess_for_title(line):
    # print line
    line = line.decode("utf8")
    string = re.sub("[\[\`\~\ \!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\_]", "", line)
    # print string
    string = re.sub("[+——！，。？?《》【】’‘、~@#￥%……&*“”（）「」／；｜|：]+".decode("utf8"), "".decode("utf8"), string)
    return string.strip()


def preprocess_for_content(line):
    line = line.decode("utf8")
    string = re.sub("[\[\`\~\ \@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\<\>\/\~\@\#\\\&\*\%\_]", "", line)
    string = re.sub("[+——，《》【】’‘、~@#￥%……&*“”（）「」／；｜|：]+".decode("utf8"), "".decode("utf8"), string)
    # string = re.sub("[\s+\/_,()-:$%^*(+\"\'\t+]+|[+——！，、《》【】’‘~@#￥%……&*“”（）；｜|：]+".decode("utf8"), "".decode("utf8"), line)
    string = re.sub("[\.\!\?]+|[！，。？?]+".decode("utf8"), ".".decode("utf8"), string)
    # string = re.sub("[\.\!]+|[！，。？?]+".decode("utf8"), "".decode("utf8"), string)
    return string.strip()


def transform_title_file(source_file, target_file):
    s_f = open(source_file, "r")
    t_f = open(target_file, 'w')
    lines = s_f.readlines()  # 读取全部内容
    for line in lines:
        # print preprocess_for_title(line)
        t_f.write(preprocess_for_title(line) + "\n")


def transform_content_file(source_file, target_file):
    s_f = open(source_file, "r")
    t_f = open(target_file, 'w')
    lines = s_f.readlines()  # 读取全部内容
    for line in lines:
        # print preprocess_for_content(line)
        t_f.write(preprocess_for_content(line) + "\n")
    # return 0


def test_for_title():
    source_file = "../data/raw_title.txt"
    target_file = "../data/title.txt"
    transform_title_file(source_file=source_file, target_file=target_file)

def test_for_content():
    source_file = "../data/raw_content.txt"
    target_file = "../data/content.txt"
    transform_content_file(source_file=source_file, target_file=target_file)

if __name__=="__main__":
    # str = '对话王劲：无人驾驶每asdfghj天能救500多条人命|AI英雄'
    # print preprocess_for_title(str)
    # test_for_title()
    test_for_content()

