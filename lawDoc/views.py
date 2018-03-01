import json

from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from lawDoc.Variable import legalDocuments, allSearchField,allSearchFieldList

# Create your views here.

# 展示首页,java版本对应路径为“/”
from lawDoc.models import SearchStruct


def index(request):
    return render(request, 'index.html')


# 首页的搜索，java版本对应路径为“indexsearch”
def indexSearch(request):
    print("1111111111111111")
    keyWord = request.POST.get('keyword')
    searchStruct = SearchStruct()
    searchStruct.allNotFieldKeyWord = keyWord.split(" ")
    print(searchStruct.allFieldKeyWord)
    legalDocuments.clear()
    searchByStrcut(searchStruct)


# 搜索结果页的重新搜索，java版本对应路径为“newsearch”
def newSearch(request):
    pass


# 搜索结果页的结果内搜索，java版本对应路径为“addsearch”
def addSearch(request):
    pass


# 加载更多，java版本对应路径为getMore
def getMore(request):
    pass


# 聚类搜索，java版本对应路径为addsearchandterm
def groupBySearch(request):
    pass


# 进入详细页面，java版本对应路径为searchresult
def getDetail(request):
    pass


# 进入推荐页面，java版本对应路径为recommondDetail
def getRecommondDetail(request):
    pass


# searchStruct 为搜索结构体，包含搜索搜索条件
def searchByStrcut(searchStruct):
    # 连接es
    es = Elasticsearch()
    # 取出searchstruct中的allFieldKeyWord
    allFieldKeyWord = searchStruct.allFieldKeyWord
    allFieldKeyWordQuery = []
    allFieldKeyWordMiniQuery = []
    # 全领域搜索的解决思路是对每个域进行搜索，之间用should连接
    for i in allFieldKeyWord:
        for j in allSearchField:
            allFieldKeyWordMiniQuery.append({"match_phrase": {j: i}})
        allFieldKeyWordQuery.append({
            "bool": {
                "should": allFieldKeyWordMiniQuery
            }
        })
        allFieldKeyWordMiniQuery = []

    query = {"query": {"bool": {"must": allFieldKeyWordQuery}}}


    #全域非搜索
    allFieldNotKeyWord=searchStruct.allNotFieldKeyWord
    allFieldNotKeyWordQuery=[]
    allFieldNotKeyWordMiniQuery=[]
    for i in allFieldNotKeyWord:
        for j in allSearchField:
            allFieldNotKeyWordMiniQuery.append({"match_phrase":{j:i}})
        allFieldNotKeyWordQuery.append({"bool":{"must_not":allFieldNotKeyWordMiniQuery}})
        allFieldNotKeyWordMiniQuery = []
    query = {"query": {"bool": {"must": allFieldNotKeyWordQuery}}}




    # 同域搜索

    # 变量：
    #     fieldKeyWord: 获取 searchStruct 中的 FieldKeyWord 列表
    #     fieldKeyWordQuery: 同域搜索 json 列表（对应 json 层: bool -> should）
    #     fieldKeyWordMiniQuery: 临时变量，用于生成每个域中都包含查询关键字的列表（对应 json 层: bool ->
    #                            should -> bool -> must）

    # 返回：
    #     fieldKeyWordQuery: 同域搜索 json 列表 （对应 json 层: bool -> should）

    fieldKeyWord = searchStruct.FieldKeyWord
    fieldKeyWordQuery = []
    # 如果 fieldKeyWord 列表不为空
    if len(fieldKeyWord) > 0:

        # 依次添加每个域
        for field in allSearchField:
            fieldKeyWordMiniQuery = []

            # 把每个关键字都加入域中
            for key in fieldKeyWord:
                fieldKeyWordMiniQuery.append({"match_phrase": {field: key}})

            # 把已经处理好的域进行 json 封装打包
            fieldKeyWordQuery.append({"bool": {"must": fieldKeyWordMiniQuery}})

        # json 封装打包
        # fieldKeyWordQueryCopy: 对 fieldKeyWordQuery 深复制
        fieldKeyWordQueryCopy = fieldKeyWordQuery[:]
        fieldKeyWordQuery = {"bool": {"should": fieldKeyWordQueryCopy}}

    # 顺序搜索

    # 变量：
    #     orderFieldKeyWord: 获取 searchStruct 中的 OrderFieldKey
    #     orderFieldKeyWordQuery: 顺序搜索 json 列表（对应 json 层: bool -> should）
    #     orderFieldKeyWordMiniQuery: 临时变量，用于生成每个域中包含查询关键字的列表（对应 json 层: bool ->
    #                                 should -> bool -> must）
    #     wildcard_str: 临时变量，用于生成正则表达式

    # 返回：
    #     orderFieldKeyWordQuery: 顺序搜索 json 列表（对应 json 层: bool -> should）

    orderFieldKeyWord = searchStruct.OrderFieldKey
    orderFieldKeyWordQuery = []
    # 如果 orderFieldKeyWord 列表不为空
    if len(orderFieldKeyWord) > 0:

        # 依次添加每个域
        for field in allSearchField:
            orderFieldKeyWordMiniQuery = []
            wildcard_str = ''

            # 把每个关键字加入域中
            for key in orderFieldKeyWord:
                orderFieldKeyWordMiniQuery.append({
                    "match_phrase": {
                        field: key
                    }
                })
                # 在每个关键字前加入 '*'
                wildcard_str += '*' + key

            # 在正则表达式最后加入 '*'
            wildcard_str += '*'
            # 把正则表达式放入 "wildcard" 层中
            orderFieldKeyWordMiniQuery.append({
                "wildcard": {
                    field + 'copy': wildcard_str
                }
            })

            # 把已经处理好的域进行 json 封装打包
            orderFieldKeyWordQuery.append({
                "bool": {
                    "must": orderFieldKeyWordMiniQuery
                }
            })

        # json 封装打包
        # orderFieldKeyWordQueryCopy: 对 orderFieldKeyWordQuery 深复制
        orderFieldKeyWordQueryCopy = orderFieldKeyWordQuery[:]
        orderFieldKeyWordQuery = {
            "bool": {
                "should": orderFieldKeyWordQueryCopy
            }
        }


    # 单领域否定搜索:输出：oneFieldKeyNotWordQuery
    if len(searchStruct.oneFieldNotKeyWord) != 0:
        oneFieldKeyWord = searchStruct.oneFieldKeyWord
        oneFieldNotKeyWord = searchStruct.oneFieldNotKeyWord
        field = allSearchFieldList[oneFieldNotKeyWord["field"]]
        oneFieldKeyNotWordMiniQuery = []
        oneFieldKeyNotWordQuery = []
        for i in oneFieldNotKeyWord["notkeywords"]:
            oneFieldKeyNotWordMiniQuery.append({"match_phrase": {field: i}})
        oneFieldKeyNotWordQuery = {
                "bool": {
                    "must_not": oneFieldKeyNotWordMiniQuery
                }

        }

    print(json.dumps(query))
    results = es.search(index='legal_index', doc_type='lagelDocument', body=json.dumps(query))['hits']['hits']


    


    for result in results:
        lines = result['_source']['byrw'].split("\n")
        print(lines)
