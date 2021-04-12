import json
from tqdm import tqdm
import jieba
from load_utils import read_stopwords
from collections import OrderedDict
import math
import time

#读入统计数据
def read_all_datas(word_info_file):
    with open(word_info_file, 'r', encoding='utf-8') as reader:
        all_datas = {}
        lines = reader.readlines()
        for line in tqdm(lines):
            pos = line.index(':')
            key = line[:pos]
            value = json.loads(line[pos+1:])
            all_datas[key] = value
    return all_datas


#找到最后一个非停用词，并返回整句话中所有的非停用词和最后一个非停用词
def get_all_words_and_last_word(text_words, stop_words):
    all_words = []  # 放非停用词，即有意义的词
    for word in text_words:
        if not ((word.isalnum()) and (not word.isdigit()) and (word not in stop_words)):
            continue
        all_words.append(word)
        last_word = word
    return all_words, last_word


#返回最后一个词的next_words的列表的前topk
def get_n_words_list_topk(topk, last_word, all_datas):

    n_words_list = None
    n_words_list = list(all_datas[last_word]['n_words'].items())

    n_words_list.sort(key=lambda x: x[1], reverse=True)
    n_words_list = n_words_list[:topk]   # 取top10
    return n_words_list


#计算每个next_words对于给定的前面的text_words的tf-idf得分
#返回一个list,里面是[(n_word1, score), (n_word2, score)....]的形式
#eg.[('思想', 4.114596727498982), ('三个', 3.7411634053738085), ('执政', 3.0941803322780133), ('原则', 2.607020052105015),.......]
def cal_res(all_words, n_words_list, all_datas):
    res = []
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
    return res



#给定文本text, 输出前topk个可能的后续词的预测
def predict_next_words(text, all_datas, topk, stop_words):
    text_words = jieba.lcut(text)
    #打分
    last_word = None
    all_words, last_word = get_all_words_and_last_word(text_words, stop_words)

    #如果没有两个以上的非停用词就返回None
    if len(all_words) <= 2:
        return None
    n_words_list = get_n_words_list_topk(topk, last_word, all_datas)
    if not n_words_list:
        return None

    #遍历第二遍，计算前面每个词的tf-idf:
    res = cal_res(all_words=all_words, n_words_list=n_words_list, all_datas=all_datas)
    return res

def predict(word_info_file, stopwords_file, topk):
    all_datas = read_all_datas(word_info_file=word_info_file)
    stop_words = read_stopwords(stopwords_file=stopwords_file)
    while True:
        text = input('请输入句子')
        start_time = time.time()
        res = predict_next_words(text=text, stop_words=stop_words, all_datas=all_datas, topk=topk)
        end_time = time.time()
        print('costing time:', end_time-start_time)
        print(res)
if __name__ == '__main__':
    word_info_file = 'all_word_info.json'
    stopwords_file = 'data/stopwords.txt'
    predict(word_info_file=word_info_file, stopwords_file=stopwords_file, topk=10)


