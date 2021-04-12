# TF-IDF Predict Next Word

Predict next word using tf-idf

### File structure

+ /data  数据文件存放目录

  + data.json   公文文件
  + stopwords.txt  停用词文件

+ load_utils.py   

  一些工具函数
  
+ get_context_wrod.py  

  统计出all_word_info.json的程序
  
+ predict_next_word_tfidf.py  

  利用all_word_info.json的统计数据计算tf-idf，预测下一个词
  
+ all_word_info.json

  整个近5w个公文文档（近200w个句子）的统计数据

+ word_info.json

  用10000个句子统计的缩略版数据，用于简单的测试，加载较快

+ readme.md 

  说明文件，此文件
