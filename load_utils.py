import jieba
import re
import json
from tqdm import tqdm

# text = '京规自发〔2021〕28号\n\n各区政府，经济技术开发区管委会，各相关委办局：\n\n　　为贯彻落实《国务院办公厅转发住房城乡建设部关于完善质量保障体系提升建筑工程品质指导意见的通知》'
# word_set = set()
# words = jieba.lcut(text)
# print(words)
# paragraph = "项目审批、信用评价、职业保险、教育培训等配套制度。\n\n\u3000\u3000权责同步与统筹推进。以给建筑师赋权作为前提，以合理化取酬作为保障，以信用监督落实责任。"




'''
prarams:data_file=data file.json
return: docs --> list of 'contents'
'''
def read_data(data_file):
    # 将data转换成docs，共45756个doc
    with open(data_file, 'r', encoding='utf-8') as reader:
        content = reader.read()
        data_dict = json.loads(content)
    docs = [a_data['content'] for a_data in data_dict]
    #print(len(docs))
    return docs

#docs = read_data(data_file)
#print(len(docs))
#paragraph = docs[0]


#将每个doc分成句子,共1795174个句子
'''
params:docs --> list of 'contents'
return:all_sents -->list: all_sents  sents of all docs
'''
def split_sents(data_file):
    # 输入一个段落，分成句子，可使用split函数来实现
    docs = read_data(data_file)
    all_sents = []
    for doc in tqdm(docs, desc='SplitSents'):
        sentences = re.split('(。|！|\!|\.|？|\?)', doc)  # 保留分割符
        for i in range(int(len(sentences) / 2)):
            sent = sentences[2 * i] + sentences[2 * i + 1]
            all_sents.append(sent.strip())
    return all_sents

'''
param:stopword_file
rtype: list:stopwords[]
'''
def read_stopwords(stopwords_file):
    stop_words = []
    with open(stopwords_file, 'r', encoding='utf-8') as reader:
        lines = reader.readlines()
        for line in lines:
            stop_words.append(line.strip())
    # print(stop_words[:100])
    # print('len:', len(stop_words))
    return stop_words




'''
param: all_sents: sentences of all docs
        stopwords_file
rtype:set() of all _words
'''
def get_word_dict(all_sents, stopwords_file):
    stop_words = read_stopwords(stopwords_file=stopwords_file)
    all_words = []
    for sent in tqdm(all_sents, desc='loading_word_dict'):
        words = set(jieba.lcut(sent))
        for word in words:
            if (word.isalnum()) and (not word.isdigit()) and (word not in stop_words):
                all_words.append(word)
    return set(all_words)

'''
writing to file
'''
def writing_word_dict_to_file(data_file, stopwords_file, word_dict_file):
    all_sents = split_sents(data_file=data_file)
    all_word_dict = get_word_dict(all_sents=all_sents, stopwords_file=stopwords_file)
    with open(word_dict_file, 'w', encoding='utf-8') as writer:
        for word in tqdm(all_word_dict, desc='writing'):
            writer.write(str(word)+'\n')

if __name__ == '__main__':
    data_file = 'data/data.json'
    stopwords_file = 'data/stopwords.txt'
    word_dict_file = 'all_word_dict.txt'
    writing_word_dict_to_file(data_file=data_file, stopwords_file=stopwords_file,word_dict_file=word_dict_file)
