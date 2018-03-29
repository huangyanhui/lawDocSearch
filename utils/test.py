import os

from gensim import corpora,models,similarities,utils

wenshu='00000412.txt'
anyou = '爆炸罪'
filepath = os.path.join(r'D:alltext',anyou)
fr = r'result' 
f = open(os.path.join(filepath,wenshu),encoding='utf-8')
lines = f.readlines()
text = []
for line in lines:#将文件中的词装入列表
     if len(line) != 1:
            # 抽掉引用法条
            if line.split('##')[0] != '引用法条' and line.split('##')[0] != '特征' and line.split('##')[0] != '案由':
                for word in line.split('##')[1].split('$'):
                    text.append(word.replace('\n', '').replace('\t', ''))
            if line.split('##')[0] == '特征':
                for word in line.split('##')[1].split('\t'):
                    text.append(word.replace('\n', '').replace('\t', ''))
            if line.split('##')[0] == '案由':
                for word in line.split('##')[1].split('\t'):
                    text.append(word.replace('\n', '').replace('\t', ''))

#到该案由路径下载入获取已经训练好的模型
output = os.path.join (fr,anyou)


# 载入字典
dictionary = corpora.Dictionary.load(os.path.join(output,"all.dic"))


# 载入TFIDF模型和索引
tfidfModel = models.TfidfModel.load(os.path.join(output,"allTFIDF.mdl"))
indexTfidf = similarities.MatrixSimilarity.load(os.path.join(output,"allTFIDF.idx"))


# # 载入LDA模型和索引
ldaModel = models.LdaModel.load(os.path.join(output,  "allLDATopic.mdl"))
indexLDA = similarities.MatrixSimilarity.load(os.path.join (output,"allLDATopic.idx"))


#query就是测试数据，先切词
query_bow = dictionary.doc2bow(text)


#使用TFIDF模型向量化
tfidfvect = tfidfModel[query_bow]


#然后LDA向量化，因为我们训练时的LDA是在TFIDF基础上做的，所以用itidfvect再向量化一次
ldavec = ldaModel[tfidfvect]


#TFIDF相似性，相似性列表记录与每份模型中的文书的相似度
simstfidf = indexTfidf[tfidfvect]


#LDA相似性，相似性列表记录与每份模型中的文书的相似度
simlda = indexLDA[ldavec]


sort_sims = sorted(enumerate(simlda), key=lambda item: -item[1])
print(sort_sims)


bianhaolda = {}
for keys in sort_sims[0:11]:
    key=keys[0]
    key=str(key)
    while len(key)<8:
        key = "0"+ key
    key = key + '.txt'
    file = open(os.path.join(filepath,key),encoding = 'UTF-8')
    lines = file.readlines()
    for line in lines:#将文件中的编号装入列表
        if len(line) != 1:
            if line.split('##')[0] == '编号':
                print(line.split('##')[1])
                bianhaolda[line.split('##')[1].strip('\n')]=keys[1]
print(bianhaolda)