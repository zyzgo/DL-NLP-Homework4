import math
import jieba
import os  # 用于处理文件路径
import re
import sys
import random
import numpy as np
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

jieba.suggest_freq('郭靖', True)
jieba.suggest_freq('黄蓉', True)
jieba.suggest_freq('杨康', True)
jieba.suggest_freq('穆念慈', True)
jieba.suggest_freq('黄药师', True)
jieba.suggest_freq('欧阳锋', True)
jieba.suggest_freq('洪七公', True)
jieba.suggest_freq('周伯通', True)
jieba.suggest_freq('柯镇恶', True)
jieba.suggest_freq('梅超风', True)

def read_novel(path_in, path_out):  # 读取语料内容
    content = []
    names = os.listdir(path_in)
    for name in names:
        novel_name = path_in + '\\' + name
        fenci_name = path_out + '\\' + name
        for line in open(novel_name, 'r', encoding='ANSI'):
            line.strip('\n')
            line = content_deal(line)
            con = jieba.cut(line, cut_all=False) # 结巴分词
            # con = content_stopword(con)
            # content.append(con)
            content.append(" ".join(con))
        with open(fenci_name, "w", encoding='utf-8') as f:
            f.writelines(content)
    return content, names


def content_deal(content):  # 语料预处理，进行断句，去除一些广告和无意义内容
    ad = ['本书来自www.cr173.com免费txt小说下载站', '更多更新免费电子书请关注www.cr173.com',
          '\u3000', '\n', '。', '？', '！', '，', '；', '：', '、', '《', '》', '“', '”', '‘', '’', '［', '］', '....', '......',
          '『', '』', '（', '）', '…', '「', '」', '\ue41b', '＜', '＞', '+', '\x1a', '\ue42b'] #去掉其中的一些无意义的词语
    for a in ad:
        content = content.replace(a, '')
    return content


def load_stopword():
    f_stop = open('cn_stopwords.txt', encoding='utf-8')
    sw = [line.strip() for line in f_stop]
    f_stop.close()
    return sw


def content_stopword(content):
    stopwords = load_stopword()
    content_new = []
    for words in content:
        if words not in stopwords:
            content_new.append(words)
    return content_new


if __name__ == '__main__':   ##
    [data_txt, files] = read_novel("金庸小说集", "output")
    #[data_txt, files] = read_novel("倚天屠龙记", "output")
    #model = Word2Vec(data_txt, vector_size=400, window=5, min_count=5, epochs=200, workers=multiprocessing.cpu_count())
    test_name = ['郭靖', '黄蓉', '杨康', '欧阳锋']
    name = "output/射雕英雄传.txt"
    model = Word2Vec(sentences=LineSentence(name), hs=1, min_count=10, window=5, vector_size=200, sg=0, epochs=200)
    for i in range(len(test_name)):
        print(test_name[i])
        req_count = 5
        for key in model.wv.similar_by_word(test_name[i], topn=20):
            if len(key[0]) == 3 or len(key[0]) == 2:
                req_count -= 1
                print(key[0], key[1])
                if req_count == 0:
                    break
    print(model.wv.similarity('黄药师', '东邪'))
    print(model.wv.similarity('欧阳锋', '西毒'))
    print(model.wv.doesnt_match(u"郭靖 黄蓉 杨康 铁木真".split()))


        # for result in model.wv.similar_by_word(test_menpai[i], topn=10):
        #     print(result[0], result[1])


