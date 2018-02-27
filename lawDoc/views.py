import json

from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from lawDoc.Variable import legalDocuments, allSearchField, allSearchFieldList

# Create your views here.

#展示首页,java版本对应路径为“/”
from lawDoc.models import SearchStruct


def index(request):
    return render(request,'index.html')

#首页的搜索，java版本对应路径为“indexsearch”
def indexSearch(request):
    print("1111111111111111")
    keyWord=request.POST.get('keyword')
    print(keyWord)
    searchStruct = SearchStruct()
    if '@' in keyWord:
        field=keyWord.split("@")[1]
        keyWord = keyWord.split("@")[0]
    else:
        field="all"
    if '!'in keyWord:
        keywords = keyWord.split("!")[0].split(" ")
        notkeywords = keyWord.split("!")[1].split(" ")
        if field == "all":
            searchStruct.allFieldKeyWord = keywords
            searchStruct.allFieldNotKeyWord = notkeywords
        else:
            searchStruct.oneFieldKeyWord = {"field":field,"keywords":keywords}
            searchStruct.oneFieldNotKeyWord = {"field":field,"notkeywords":notkeywords}

    print("****************/n")
    print(searchStruct.oneFieldKeyWord)
    print("****************/n")
    print(searchStruct.oneFieldNotKeyWord)
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
    #取出searchstruct中的allFieldKeyWord
    allFieldKeyWord=searchStruct.allFieldKeyWord
    allFieldKeyWordQuery=[]
    allFieldKeyWordMiniQuery=[]
    #单领域否定搜索
    if len(searchStruct.oneFieldNotKeyWord) != 0:
        oneFieldKeyWord = searchStruct.oneFieldKeyWord
        oneFieldNotKeyWord = searchStruct.oneFieldNotKeyWord
        field = allSearchFieldList[oneFieldNotKeyWord["field"]]
        print(field)
        oneFieldKeyNotWordMiniQuery = []
        oneFieldKeyNotWordQuery = []
        for i in oneFieldNotKeyWord["notkeywords"]:
            print(i)
            oneFieldKeyNotWordMiniQuery.append({"match_phrase":{field:i}})
        query = {
            "query":{
                "bool":{
                    "must_not":oneFieldKeyNotWordMiniQuery
                }
            }
        }
        print(json.dumps(query))
        results = es.search(index='legal_index', doc_type='lagelDocument', body=json.dumps(query))['hits']['hits']


        for result in results:
            lines=result['_source']['byrw'].split("\n")
            print(lines)








    # for i in allFieldKeyWord:
    #     for j in allSearchField:
    #         allFieldKeyWordMiniQuery.append({"match_phrase":{j:i}})
    #     allFieldKeyWordQuery.append({"bool":{"should":allFieldKeyWordMiniQuery}})
    #
    # query = {
    # "query": {
    #     "bool": {
    #         "must": allFieldKeyWordQuery
    #     }
    # }
    # }
    #
    # print(json.dumps(query))
    # results = es.search(index='legal_index', doc_type='lagelDocument', body=json.dumps(query))['hits']['hits']
    #
    #
    # for result in results:
    #     lines=result['_source']['byrw'].split("\n")
    #     print(lines)
