import jieba.posseg as pseg
import codecs
from gensim import corpora,models,similarities

novel_file = 'data/novel'
book_file='data/booknovel'
stop='data/stopwords'
stopwords = codecs.open(stop,'r',encoding='utf8').readlines()
stopwords = [ w.strip() for w in stopwords ]
stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']

def redfile(str):
    info=[]
    with open(str,encoding='utf-8') as f:
        for line in f:
            item=line.split(' ')
            info.append(item)
    return info

def changedict(info):
    dictbook={}
    i=0
    for item in info:
        dictbook[i]=item
        i=i+1
    return dictbook


#########################读文件为字典##############################
def books_factory(filename, books_factory):
    #books_factory为字典
    """获取书籍基础信息，用于使用编号来提取书籍具体信息"""
    with open(filename, encoding='utf-8') as f:
        i=0
        for line in f.readlines():
            col = line.split(' ')
            index =i
            i=i+1
            books_factory.setdefault(index, [])
            #get() 方法类似, 如果键不存在于字典中，将会添加键并将值设为默认值。
            books_factory[index] = col
    return books_factory
###############################################################################
#将读取的列表书籍信息，转化为字典类型，key为在总的列表文件中的顺序，值为分词（经过停用词之后的）
def tostringdict(listInfo,stopwords,stop_flag):
    dictInfo={}
    i=0
    for item in listInfo:
        result=[]
        value=item[3]+item[4]+item[5]+item[8]
        words=pseg.cut(value)
        for word, flag in words:
            if flag not in stop_flag and word not in stopwords:
                result.append(word)
        dictInfo[i]=result
        i=i+1
    return dictInfo
###########################################################################
#建立词袋与TF-IDF模型,并计算相似度 返回相似度
def similary(dictInfo,key):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    corpus=[]
    for item in dictInfo:
        corpus.append(dictInfo[item])
    dictionary = corpora.Dictionary(corpus)
    doc_vectors = [dictionary.doc2bow(text) for text in corpus]
    tfidf = models.TfidfModel(doc_vectors)
    tfidf_vectors = tfidf[doc_vectors]
    #要计算相似度的书籍信息
    query=dictInfo[key]
    query_bow = dictionary.doc2bow(query)
    index = similarities.MatrixSimilarity(tfidf_vectors)
    sims = index[query_bow]
    listsimilary=list(enumerate(sims))
    #print(listsimilary)
    return listsimilary
################################算出推荐结果#####################################
def commend(listsimlary,dictInfo):
    result={}
    #####################排序##########################
    for i in range(0,len(listsimlary)):
        for j in range(i+1,len(listsimlary)):
            if listsimlary[j][1]>=listsimlary[i][1]:
                temp=listsimlary[j]
                listsimlary[j]=listsimlary[i]
                listsimlary[i]=temp
    ##################找结果###################33
    for i in range(1,6):
        for key in dictInfo:
            if key==listsimlary[i][0]:
                result[key]=dictInfo[key]
    return result
def recommend(listInfo,index):#读到的文件，推荐的书的序号
    dictInfo = tostringdict(listInfo, stopwords, stop_flag)
    listimilary = similary(dictInfo, index)
    dictbook = changedict(listInfo)
    result=commend(listimilary, dictbook)
    return result

