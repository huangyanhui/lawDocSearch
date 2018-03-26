import os
import jieba
import jieba.analyse

source_path = '/home/cowlog/Project/刑事/提取/'
target_path = '/home/cowlog/Project/刑事/分词/'
stopped_word = '/home/cowlog/Dropbox/Project/nltk/chinese_stopped.txt'

ignored_list = set(['案由', '引用法条', '特征'])

jieba.analyse.set_stop_words(stopped_word)

for path in os.listdir(source_path):
    source_file = open(source_path + path, 'r')
    target_file = open(target_path + path, 'w')

    for line in source_file.readlines():
        key, content = line.split('##')
        if key in ignored_list:
            target_file.write(key + '##' + content + '\n')
        else:
            # seg_list = jieba.cut(content, cut_all=False)
            seg_list = jieba.analyse.extract_tags(content)
            target_file.write(key + '##' + '$'.join(seg_list) + '\n')

    source_file.close()
    target_file.close()
