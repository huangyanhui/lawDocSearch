import json

from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from lawDoc.Variable import legalDocuments, allSearchField

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
    searchStruct.allFieldKeyWord = keyWord.split(" ")
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

    # 同域搜索
    fieldKeyWord = searchStruct.FieldKeyWord
    fieldKeyWordQuery = []
    if len(fieldKeyWord) > 0:

        for field in allSearchField:
            fieldKeyWordMiniQuery = []

            for key in fieldKeyWord:
                fieldKeyWordMiniQuery.append({"match_phrase": {field: key}})

            fieldKeyWordQuery.append({"bool": {"must": fieldKeyWordMiniQuery}})

        must_list = []
        must_list.append({"bool": {"should": fieldKeyWordQuery}})

        query = {"query": {"bool": {"must": must_list}}}

    # 顺序搜索
    orderFieldKeyWord = searchStruct.OrderFieldKey
    orderFieldKeyWordQuery = []
    if len(orderFieldKeyWord) > 0:

        for field in allSearchField:
            orderFieldKeyWordMiniQuery = []
            wildcard_str = ''

            for key in orderFieldKeyWord:
                orderFieldKeyWordMiniQuery.append({
                    "match_phrase": {
                        field: key
                    }
                })
                wildcard_str += '*' + key

            wildcard_str += '*'
            orderFieldKeyWordMiniQuery.append({
                "wildcard": {
                    field + 'copy': wildcard_str
                }
            })
            orderFieldKeyWordQuery.append({
                "bool": {
                    "must": orderFieldKeyWordMiniQuery
                }
            })

        must_list = []
        must_list.append({"bool": {"should": orderFieldKeyWordQuery}})

        query = {"query": {"bool": {"must": must_list}}}

    print(json.dumps(query, ensure_ascii=False))
    results = es.search(
        index='legal_index',
        doc_type='lagelDocument',
        body=json.dumps(query, ensure_ascii=False))['hits']['hits']

    for result in results:
        lines = result['_source']['byrw'].split("\n")
        print(lines)
