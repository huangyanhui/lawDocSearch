from gensim import corpora, models, similarities, utils
import os

# # 重新编号
allFile = os.listdir(r'D:alltext2')
filePath = r'D:alltext2'
resultFile = r'result'
for fileOne in allFile:  # 遍历整个一级文件夹
    train_set = []
    tmp_pathall = os.path.join(filePath, fileOne)
    fileTwo = os.listdir(tmp_pathall)
    i = 0
    for fileThree in fileTwo:  # 遍历单个案由的所有文件
        k = len(str(i))
        j = ''
        for co in range(0, 8 - k):
            j = j + '0'
        j = j + str(i) + '.txt'
        tmp_path = os.path.join(tmp_pathall, fileThree)
        os.rename(tmp_path, os.path.join(tmp_pathall, j))
        i = i + 1
# 收集训练集
allFile = os.listdir(r'D:alltext2')
filePath = r'D:alltext2'
resultFile = r'result'
for fileOne in allFile:  # 遍历整个一级文件夹
    train_set = []
    tmp_pathall = os.path.join(filePath, fileOne)
    anyouDir = os.listdir(tmp_pathall)
    if len(anyouDir) <= 10:
        continue
    for fileTwo in anyouDir:  # 遍历单个案由的所有文件
        tmp_path = os.path.join(tmp_pathall, fileTwo)
        f = open(tmp_path, encoding='utf-8')
        lines = f.readlines()
        text = []
        # 将文件中的词装入列表
        for line in lines:
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
        f.close()
        train_set.append(text)
    output = os.path.join(resultFile, fileOne)  # 输出文件目录
    if not os.path.exists(output):
        os.makedirs(output)
        # 生成字典
    dictionary = corpora.Dictionary(train_set)

    # 去除极低频的杂质词
    dictionary.filter_extremes(no_below=1, no_above=1, keep_n=None)



    # 将词典保存下来，方便后续使用
    dictionary.save(os.path.join(output, "all.dic"))

    #生成数字语料
    corpus = [dictionary.doc2bow(text) for text in train_set]


    # 使用数字语料生成TFIDF模型
    tfidfModel = models.TfidfModel(corpus)


    # 存储tfidfModel
    tfidfModel.save(os.path.join(output, "allTFIDF.mdl"))


    # 把全部语料向量化成TFIDF模式，这个tfidfModel可以传入二维数组
    tfidfVectors = tfidfModel[corpus]


    # 建立索引并保存
    indexTfidf = similarities.MatrixSimilarity(tfidfVectors)
    indexTfidf.save(os.path.join(output, "allTFIDF.idx"))


    # 通过TFIDF向量生成LDA模型，id2word表示编号的对应词典，num_topics表示主题数，我们这里设定的100，主题太多时间受不了。
    lda = models.LdaModel(tfidfVectors, id2word=dictionary, num_topics=100)


    # 把模型保存下来
    lda.save(os.path.join(output, "allLDATopic.mdl"))


    # 把所有TFIDF向量变成LDA的向量
    corpus_lda = lda[tfidfVectors]


    # 建立索引，把LDA数据保存下来
    indexLDA = similarities.MatrixSimilarity(corpus_lda)
    indexLDA.save(os.path.join(output, "allLDATopic.idx"))