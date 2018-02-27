import json

from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from lawDoc.Variable import legalDocuments, allSearchField, allSearchFieldDict


# Create your views here.

#展示首页,java版本对应路径为“/”
from lawDoc.models import SearchStruct


def index(request):
    return render(request,'index.html')

#首页的搜索，java版本对应路径为“indexsearch”
def indexSearch(request):
    print("1111111111111111")
    searchStruct=SearchStruct()
    keyWord=request.POST.get('keyword')
    #keyWord = "杀人 放火@本院认为"
    #构建搜索结构
    if "@" in keyWord:
        if "!" in keyWord:
            pass
        else:
            searchStruct.oneFieldKeyWord = {
                "field":keyWord.split("@")[1],
                "keyword":keyWord.split("@")[0].split(" ")
            }
    else:
        if "!" in keyWord:
            pass
        else:
            searchStruct.allFieldKeyWord=keyWord.split(" ")
            print(searchStruct.allFieldKeyWord)

    legalDocuments.clear()
    searchByStrcut(searchStruct)


#搜索结果页的重新搜索，java版本对应路径为“newsearch”
def newSearch(request):
    pass

#搜索结果页的结果内搜索，java版本对应路径为“addsearch”
def addSearch(request):
    pass

#加载更多，java版本对应路径为getMore
def getMore(request):
    pass

#聚类搜索，java版本对应路径为addsearchandterm
def groupBySearch(request):
    pass

#进入详细页面，java版本对应路径为searchresult
def getDetail(request):
    pass

#进入推荐页面，java版本对应路径为recommondDetail
def getRecommondDetail(request):
    pass

#searchStruct为搜索结构体，包含搜索搜索条件
def searchByStrcut(searchStruct):
    #连接es
    es = Elasticsearch()
    # #取出searchstruct中的allFieldKeyWord
    # allFieldKeyWord=searchStruct.allFieldKeyWord
    # allFieldKeyWordQuery=[]
    # allFieldKeyWordMiniQuery=[]
    # #全领域搜索的解决思路是对每个域进行搜索，之间用should连接
    # for i in allFieldKeyWord:
    #     for j in allSearchField:
    #         allFieldKeyWordMiniQuery.append({"match_phrase":{j:i}})
    #     allFieldKeyWordQuery.append({"bool":{"should":allFieldKeyWordMiniQuery}})

    #单领域搜索
    if len(searchStruct.oneFieldKeyWord) != 0:
        oneFieldKeyWord = searchStruct.oneFieldKeyWord["keyword"]
        oneFieldKeyWordQuery = []
        field = allSearchFieldDict.get(searchStruct.oneFieldKeyWord["field"])
        for i in oneFieldKeyWord:
            oneFieldKeyWordQuery.append({"match_phrase":{field:i}})
        query = {
        "query": {
            "bool": {
                "must": oneFieldKeyWordQuery
            }
        }
    }
    print(json.dumps(query))
    results = es.search(index='legal_index', doc_type='lagelDocument', body=json.dumps(query))['hits']['hits']

    for result in results:
        lines=result['_source']['byrw'].split("\n")
        print(lines)

