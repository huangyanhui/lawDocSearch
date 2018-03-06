import json

import time

import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from elasticsearch import Elasticsearch
import pdfkit

from lawDoc.Variable import legalDocuments, allSearchField, allSearchFieldList, countResults

from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# 展示首页,java版本对应路径为“/”
from lawDoc.models import SearchStruct, LegalDocument


def index(request):
    return render(request, 'index.html')


# 首页的搜索，java版本对应路径为“indexsearch”
def indexSearch(request):
    keyWord = request.POST.get('keyword')
    searchStruct = SearchStruct()
    searchStruct.allFieldKeyWord = keyWord.split(" ")
    legalDocuments.clear()
    searchByStrcut(searchStruct)
    return render(request, "searchresult.html",
                  {"LegalDocList": legalDocuments,"countResults":countResults})


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


@csrf_exempt
# 进入详细页面，java版本对应路径为searchresult
def getDetail(request):
    if request.method == "POST":
        legalDocuments_pos = int(request.POST["legalDocuments_id"])
        print(legalDocuments_pos)
        legalDocument = legalDocuments[legalDocuments_pos]
        return render(request, "resultDetail.html",
                      {"legaldoc": legalDocument,
                       "legalDocuments_id": legalDocuments_pos})
    else:
        return render(request, "resultDetail.html")


def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

@csrf_exempt
def download(request):
    if request.method == "POST":
        print("abcabc" + request.POST["legalDocuments_id"])
        legalDocuments_pos = int(request.POST["legalDocuments_id"])
        print("abc" + str(legalDocuments_pos))
        legalDocument = legalDocuments[legalDocuments_pos]
    # 临时文件名
    curr_date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    css = r'static\css\showDetail.css'
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    path_wk = r'C:\Users\jeafi\Desktop\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 安装位置
    config = pdfkit.configuration(wkhtmltopdf=path_wk)
    # 读文件并且替换动态内容
    fp = open("pdf.html", 'w', encoding='utf-8')  # 打开你要写得文件test2.txt
    lines = open('demo.html', 'r', encoding='utf-8').readlines()  # 打开文件，读入每一行
    for s in lines:
        fp.write(s.replace("标题", legalDocument.bt)
                 .replace('diyu', legalDocument.dy)
                .replace('anhao',legalDocument.ah)
                 .replace('dangshirenxingxi', legalDocument.dsrxx)
                 .replace('anjianmiaoshu', legalDocument.ajms)
                 .replace('shenlijingguo', legalDocument.sljg)
                 .replace('yishenqingqiuqingkuang', legalDocument.ysqqqk)
                 .replace('yishendabianqingkuang', legalDocument.ysdbqk)
                 .replace('yishenfayuanchaming', legalDocument.ysfycm)
                 .replace('yishenfayuanrenwei', legalDocument.ysfyrw)
                 .replace('ershenqingqiuqingkuang', legalDocument.esqqqk)
                 .replace('benyuanchaming', legalDocument.bycm)
                 .replace('benyuanrenwei', legalDocument.byrw)
                 .replace('shenpanjieguo', legalDocument.spjg)
                 .replace('shenpanrenyuan', legalDocument.spry)
                 .replace('shenpanriqi', legalDocument.sprq)
                 .replace('shujiyuan', legalDocument.sjy)
                 .replace('xiangguanfatiao', legalDocument.xgft))  # replace是替换，write是写入
    fp.close()  # 关闭文件
    outpath = 'out%s.pdf' % (curr_date)
    pdfkit.from_file('pdf.html', options=options, css=css, output_path=outpath, configuration=config)
    # 文件下载
    file =open( '%s'%(outpath),'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"'%(outpath)
    return response


# 进入推荐页面，java版本对应路径为recommondDetail
def getRecommondDetail(request):
    pass


# 全领域搜索的解决思路是对每个域进行搜索，之间用should连接
def allFieldSearch(searchStruct):
    allFieldKeyWord = searchStruct.allFieldKeyWord
    allFieldKeyWordQuery = []
    allFieldKeyWordMiniQuery = []
    for i in allFieldKeyWord:
        for j in allSearchField:
            allFieldKeyWordMiniQuery.append({"match_phrase": {j: i}})
        allFieldKeyWordQuery.append({
            "bool": {
                "should": allFieldKeyWordMiniQuery
            }
        })
        allFieldKeyWordMiniQuery = []
    return allFieldKeyWordQuery


# 全域非搜索
def allFieldNotSearch(searchStruct):
    allFieldNotKeyWord = searchStruct.allFieldNotKeyWord
    allFieldNotKeyWordQuery = []
    allFieldNotKeyWordMiniQuery = []
    for i in allFieldNotKeyWord:
        for j in allSearchField:
            allFieldNotKeyWordMiniQuery.append({"match_phrase": {j: i}})
        allFieldNotKeyWordQuery.append({
            "bool": {
                "must_not": allFieldNotKeyWordMiniQuery
            }
        })
        allFieldNotKeyWordMiniQuery = []

    return allFieldNotKeyWordQuery


# 单领域搜索
def oneFieldSearch(searchStruct):
    oneFieldKeyWordQuery = []
    oneFieldKeyWordMiniQuery = []
    oneFieldKeyWord = searchStruct.oneFieldKeyWord
    # oneFieldKeyWord = {"byrw" :["盗窃", "窃取"], "bt": ["盗窃"]}
    fieldSet = oneFieldKeyWord.keys()
    for field in fieldSet:
        for keyWord in oneFieldKeyWord[field]:
            oneFieldKeyWordMiniQuery.append({"match_phrase": {field: keyWord}})
        oneFieldKeyWordQuery.append({
            "bool": {
                "must": oneFieldKeyWordMiniQuery
            }
        })
        oneFieldKeyWordMiniQuery = []
    return oneFieldKeyWordQuery


# 同域搜索
def fieldSearch(searchStruct):
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
    return fieldKeyWordQuery


# 顺序搜索
def orderFieldSearch(searchStruct):
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

    return orderFieldKeyWordQuery


# 单领域否定搜索:输出：oneFieldKeyNotWordQuery
def oneFieldNotSearch(searchStruct):
    oneFieldKeyNotWordQuery = []
    if len(searchStruct.oneFieldNotKeyWord) != 0:
        oneFieldKeyWord = searchStruct.oneFieldKeyWord
        oneFieldNotKeyWord = searchStruct.oneFieldNotKeyWord
        field = allSearchFieldList[oneFieldNotKeyWord["field"]]
        oneFieldKeyNotWordMiniQuery = []

        for i in oneFieldNotKeyWord["notkeywords"]:
            oneFieldKeyNotWordMiniQuery.append({"match_phrase": {field: i}})
        oneFieldKeyNotWordQuery = {
            "bool": {
                "must_not": oneFieldKeyNotWordMiniQuery
            }
        }
    return oneFieldKeyNotWordQuery


# searchStruct 为搜索结构体，包含搜索搜索条件
def searchByStrcut(searchStruct):
    # 连接es
    es = Elasticsearch()
    # 取出searchstruct中的allFieldKeyWord
    allFieldKeyWordQuery = allFieldSearch(searchStruct)
    allFieldNotKeyWordQuery = allFieldNotSearch(searchStruct)
    oneFieldKeyWordQuery = oneFieldSearch(searchStruct)
    fieldKeyWordQuery = fieldSearch(searchStruct)
    orderFieldKeyWordQuery = orderFieldSearch(searchStruct)
    oneFieldKeyNotWordQuery = oneFieldNotSearch(searchStruct)

    query = {
        "query": {
            "bool": {
                "must": [
                    allFieldKeyWordQuery, allFieldNotKeyWordQuery,
                    oneFieldKeyWordQuery, fieldKeyWordQuery,
                    orderFieldKeyWordQuery, oneFieldKeyNotWordQuery
                ]
            }
        },
        "aggs": {
            "fycj": {
                "terms": {
                    "field": "fycj"
                }
            },
            "wslx":{
                "terms": {
                    "field": "wslx"
                }
            },
            "nf":{
                "terms": {
                    "field": "nf"
                }

            },
            "ay":{
                "terms": {
                    "field": "ay"
                }

            },
            "dy":{
                "terms": {
                    "field": "dy"
                }

            },
            "slcx":{
                "terms": {
                    "field": "slcx"
                }

            }

        }
    }

    print(json.dumps(query))

    searchResults=es.search(
        index='legal_index', doc_type='lagelDocument',
        body=json.dumps(query))

    results = searchResults['hits']['hits']
    countResults['dy']=searchResults['aggregations']['dy']['buckets']
    countResults['nf'] = searchResults['aggregations']['nf']['buckets']
    countResults['ay'] = searchResults['aggregations']['ay']['buckets']
    countResults['fycj'] = searchResults['aggregations']['fycj']['buckets']
    countResults['slcx'] = searchResults['aggregations']['slcx']['buckets']
    countResults['wslx'] = searchResults['aggregations']['wslx']['buckets']




    for result in results:
        legalDoc = LegalDocument()
        legalDoc.fy = result['_source']['fy']
        legalDoc.dsrxx = result['_source']['dsrxx']
        legalDoc.ah = result['_source']['ah']
        legalDoc.spry = result['_source']['spry']
        legalDoc.ysfycm = result['_source']['ysfycm']
        legalDoc.ysqqqk = result['_source']['ysqqqk']
        legalDoc.byrw = result['_source']['byrw']
        legalDoc.spjg = result['_source']['spjg']
        legalDoc.ysdbqk = result['_source']['ysdbqk']
        legalDoc.esqqqk = result['_source']['esqqqk']
        legalDoc.ysfyrw = result['_source']['ysfyrw']
        legalDoc.wslx = result['_source']['wslx']
        legalDoc.ajms = result['_source']['ajms']
        legalDoc.xgft = result['_source']['xgft']
        legalDoc.sprq = result['_source']['sprq']
        legalDoc.sljg = result['_source']['sljg']
        legalDoc.bycm = result['_source']['bycm']
        legalDoc.sjy = result['_source']['sjy']
        legalDoc.bt = result['_source']['bt']
        legalDoc.dy = result['_source']['dy']
        legalDoc.nf = result['_source']['nf']
        legalDoc.slcx = result['_source']['slcx']
        legalDoc.ay = result['_source']['ay']
        legalDoc.ft = result['_source']['ft']
        legalDoc.tz = result['_source']['tz']
        legalDoc.fycj=result['_source']['fycj']
        legalDocuments.append(legalDoc)
    print(results)

    return legalDocuments,countResults
