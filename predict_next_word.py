import json
from tqdm import tqdm
import jieba
from load_utils import read_stopwords
from collections import OrderedDict
import math

text = '我国是社会主义国家，坚持经济'

with open('all_word_info.json', 'r', encoding='utf-8') as reader:
    all_datas = {}
    lines = reader.readlines()
    for line in tqdm(lines):
        pos = line.index(':')
        key = line[:pos]
        value = json.loads(line[pos+1:])
        all_datas[key] = value

stop_words = read_stopwords(stopwords_file='data/stopwords.txt')

text_words = jieba.lcut(text)
#打分
last_word = None
#遍历一次找到最后一个非停用词

all_words = []  #放非停用词，即有意义的词
for word in text_words:
    if not ((word.isalnum()) and (not word.isdigit()) and (word not in stop_words)):
        continue
    all_words.append(word)
    last_word = word


n_words_list = None
if last_word is not None:
    n_words_list = list(all_datas[last_word]['n_words'].items())
    n_words_list.sort(key=lambda x: x[1], reverse=True)
    n_words_list = n_words_list[:10]   # 取top10

#print(n_words_list)


#遍历第二遍，计算前面每个词的tf-idf:
res = []
if n_words_list:
    co_words = None
    #遍历next_words
    for item in n_words_list:
        n_word, n_word_times = item

        #得到next_word的出现多少句话的次数
        sentences_with_n_word = all_datas[n_word]['nums']
        #print(sentences_with_n_word)
        #找到next_word的共现co_words中出现最多的次数
        co_words_times = list(all_datas[n_word]['co_words'].values())
        max_times = max(co_words_times)  #也是tf的分母
        #得到共现词
        co_words = all_datas[n_word]['co_words']
        #计算前面每个词的tf-idf
        score_for_n_word = 0
        for text_word in all_words:
            # text_word在next_word的co_words中的共现次数
            text_word_times = co_words.get(text_word, 0)  #tf的分子,如果没共现过就为0
            tf_value = text_word_times / max_times  #tf值
            idf_value = math.log((sentences_with_n_word + 1) / (text_word_times + 1)) + 1
            tf_idf_value = tf_value * idf_value
            score_for_n_word += tf_idf_value
        res.append((n_word, score_for_n_word))
    res.sort(key=lambda x:x[1], reverse=True)
    print(text)
    print(res)

