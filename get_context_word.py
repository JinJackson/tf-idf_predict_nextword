from load_utils import split_sents, read_stopwords
import jieba
from tqdm import tqdm
import json
import random


# def get_word_list(word_dict_file):
#     all_words = []
#     with open(word_dict_file, 'r', encoding='utf-8') as reader:
#         lines = reader.readlines()
#         for line in lines:
#             word = line.strip()
#             if word.isalnum() and not word.isdigit():
#                 all_words.append(word)
#     return all_words
#
# word_list = get_word_list(word_dict_file=word_dict_file)



#使用的数据量大小,总共将近200w条
data_size = 200000

def get_word_info(data_file, stopwords_file):
    dict = {}
    stop_words = read_stopwords(stopwords_file=stopwords_file)

    all_sents = split_sents(data_file)
    random.shuffle(all_sents)
    print(len(all_sents))

    for sent in tqdm(all_sents[:data_size], desc='counting'):
        words = jieba.lcut(sent)
        words_set = set(words)

        #一次遍历 计算word后面词出现频率
        for i in range(len(words)):
            #当前词为word
            word = words[i]
            if not ((word.isalnum()) and (not word.isdigit()) and (word not in stop_words)):
                continue
            if dict.get(word, 0) == 0:
                dict[word] = {'nums': 0, 'n_words': {}, 'co_words': {}}
            if i == len(words)-1:
                break
            else:
                n_word = words[i+1]
                if not ((n_word.isalnum()) and (not n_word.isdigit()) and (n_word not in stop_words)):
                    continue
                dict[word]['n_words'][n_word] = dict[word]['n_words'].get(n_word, 0) + 1

        #第二次遍历 计算word的句子出现次数，以及词共现次数
        for word in words_set:
            if not ((word.isalnum()) and (not word.isdigit()) and (word not in stop_words)):
                continue
            dict[word]['nums'] += 1
            #遍历得到共现次数
            for co_word in words_set:
                if not ((co_word.isalnum()) and (not co_word.isdigit()) and not (co_word in stop_words)):
                    continue
                if co_word == word:
                    continue
                dict[word]['co_words'][co_word] = dict[word]['co_words'].get(co_word, 0) + 1
    return dict

def writing_word_info(all_word_info, written_file):
    with open(written_file, 'w', encoding='utf-8') as writer:
        for key in all_word_info:
            a_dict = json.dumps(all_word_info[key], ensure_ascii=False)
            res = key + ':' + a_dict
            writer.write(res + '\n')
        # json_data = json.dumps(all_word_info, ensure_ascii=False)
        # print(json_data)
        # writer.write(json_data)


if __name__ == '__main__':
    data_file = 'data/data.json'
    written_file = 'word_info_middle.json'
    stopwords_file = 'data/stopwords.txt'

    all_word_info = get_word_info(data_file, stopwords_file)
    writing_word_info(all_word_info, written_file)
