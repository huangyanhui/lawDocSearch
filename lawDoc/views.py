import json
import time
import os
import pdfkit
import gc

from django.shortcuts import render
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
from elasticsearch import Elasticsearch
from lawDoc.Variable import legalDocuments, allSearchField, \
    allSearchFieldList, countResults, resultCount, allSearchFieldListR, \
    exceptionAY
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

from gensim import corpora,models,similarities,utils


# Create your views here.

# 展示首页,java版本对应路径为“/”
from lawDoc.models import SearchStruct, LegalDocument
from utils.elastic_search import ElasticSearchClient
from gensim import corpora,models,similarities,utils

searchStruct = SearchStruct()


def index(request):
    # 已经登录或已经访问过
    # if 'username' in request.session and request.session['username'] != '':
    # if 'username' in request.session:
    allowed_count = request.session[
        'allowed_count'] if 'allowed_count' in request.session else 3
    username = request.session[
        'username'] if 'username' in request.session else ''
    identity = request.session[
        'identity'] if 'identity' in request.session else 1
    # 未登录，默认为普通用户
    # else:
    #     allowed_count = 3
    #     username = ''
    #     identity = 1

    # 测试设置 allowed_count 为 9999999999999
    # DEBUG 语句
    # allowed_count = 9999999999999
    # DEBUG 语句

    request.session['allowed_count'] = allowed_count
    request.session['username'] = username
    request.session['identity'] = identity

    # print('allowed_count' + str(allowed_count))

    return render(request, 'index.html', {
        'username': username,
        'allowed_count': allowed_count,
        'identity': identity
    })


# 搜索结构体的构造
def buildSearchStruct(queryString):
    keyword = queryString.split('@')[0]
    if '@' in queryString:
        field = allSearchFieldList[queryString.split('@')[1]]
    else:
        field = 'all'
    if '!' in keyword:
        if keyword.split('!')[0] != '':
            keywords = keyword.split('!')[0].split(' ')
            notkeywords = keyword.split('!')[1].split(' ')
            if field == 'all':
                searchStruct.allFieldKeyWord = searchStruct.allFieldKeyWord + keywords
                searchStruct.allFieldNotKeyWord = searchStruct.allFieldNotKeyWord + notkeywords
            else:

                if (field in searchStruct.oneFieldKeyWord) and len(
                        searchStruct.oneFieldKeyWord[field]) != 0:
                    keywords += searchStruct.oneFieldKeyWord[field]
                searchStruct.oneFieldKeyWord = {field: keywords}
                if (field in searchStruct.oneFieldNotKeyWord) and len(
                        searchStruct.oneFieldNotKeyWord[field]) != 0:
                    notkeywords += searchStruct.oneFieldNotKeyWord[field]
                searchStruct.oneFieldNotKeyWord = {field: notkeywords}

        else:
            notkeywords = keyword.split('!')[1].split(' ')
            if field == 'all':
                searchStruct.allFieldNotKeyWord = searchStruct.allFieldNotKeyWord + notkeywords
            else:

                if (field in searchStruct.oneFieldNotKeyWord) and len(
                        searchStruct.oneFieldNotKeyWord[field]) != 0:
                    notkeywords += searchStruct.oneFieldNotKeyWord[field]
                searchStruct.oneFieldNotKeyWord = {field: notkeywords}

    elif '~' in keyword:
        keywords = keyword.replace('~', ' ').split(' ')
        searchStruct.FieldKeyWord = searchStruct.FieldKeyWord + keywords
    elif '>' in keyword:
        keywords = keyword.replace('>', ' ').split(' ')
        searchStruct.OrderFieldKey = searchStruct.OrderFieldKey + keywords
    else:
        keywords = keyword.split(' ')
        if field == 'all':
            searchStruct.allFieldKeyWord = searchStruct.allFieldKeyWord + keywords

        else:

            if (field in searchStruct.oneFieldKeyWord) and len(
                    searchStruct.oneFieldKeyWord[field]) != 0:
                keywords += searchStruct.oneFieldKeyWord[field]
            searchStruct.oneFieldKeyWord = {field: keywords}

    return searchStruct


# 首页的搜索，java版本对应路径为“indexsearch”
def indexSearch(request):
    # 每次搜索减 1 次可用次数
    request.session['allowed_count'] -= 1
    if request.session['allowed_count'] < 0:
        if request.session['username'] == '':
            return render(request, 'account/login.html')
        else:
            return render(request, 'tips.html')

    keyWord = request.POST.get('keyword')
    global searchStruct
    searchStruct.clear()
    searchStruct = buildSearchStruct(keyWord)
    legalDocuments.clear()
    searchByStrcut(searchStruct)

    length = 10 if len(legalDocuments) > 10 else len(legalDocuments)
    # 生成用于产生标签的语句
    oneField = []
    for field in searchStruct.oneFieldKeyWord.keys():
        str = ""
        for key in searchStruct.oneFieldKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneField.append(str)
    oneFieldnot = []
    for field in searchStruct.oneFieldNotKeyWord.keys():
        str = "!"
        for key in searchStruct.oneFieldNotKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneFieldnot.append(str)

    return render(
        request, "searchresult.html", {
            "LegalDocList": legalDocuments[0:length:],
            "countResults": countResults,
            "resultCount": resultCount,
            "searchStruct": searchStruct,
            "onefield": oneField,
            "onefieldnot": oneFieldnot,
        })


# 点击搜索框下的小标签
def searchlabel(request):
    # 每次搜索减 1 次可用次数
    request.session['allowed_count'] -= 1
    if request.session['allowed_count'] < 0:
        if request.session['username'] == '':
            return render(request, 'account/login.html')
        else:
            return render(request, 'tips.html')
    # 遍历检查，点击哪个标签就会在搜索体中删除该标签
    label = request.POST.get('allFieldKeyWord')
    if (label):
        searchStruct.allFieldKeyWord.remove(label)
    label = request.POST.get('allFieldNotKeyWord')
    if (label):
        searchStruct.allFieldNotKeyWord.remove(label)
    label = request.POST.get('FieldKeyWord')
    if (label == "fieldSearch"):
        searchStruct.FieldKeyWord = []
    label = request.POST.get('OrderFieldKey')
    if (label == "orderField"):
        searchStruct.OrderFieldKey = []
    label = request.POST.get('oneFieldKeyWord')
    if (label):
        field = label.split('@')[1]
        searchStruct.oneFieldKeyWord.pop(allSearchFieldList[field])
    label = request.POST.get('oneFieldnNotKeyWord')
    if (label):
        field = label.split('@')[1]
        searchStruct.oneFieldNotKeyWord.pop(allSearchFieldList[field])
    legalDocuments.clear()
    if len(searchStruct.OrderFieldKey) \
            or len(searchStruct.FieldKeyWord)\
            or len(searchStruct.oneFieldNotKeyWord)\
            or len(searchStruct.allFieldNotKeyWord)\
            or len(searchStruct.oneFieldKeyWord)\
            or len(searchStruct.allFieldKeyWord):
        print()
    else:
        return render(
            request, 'index.html', {
                'username': request.session['username'],
                'alowed_count': request.session['allowed_count'],
                'identity': request.session['identity']
            })
    searchByStrcut(searchStruct)
    length = 10 if len(legalDocuments) > 10 else len(legalDocuments)
    # 生成用于产生标签的语句
    oneField = []
    for field in searchStruct.oneFieldKeyWord.keys():
        str = ""
        for key in searchStruct.oneFieldKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneField.append(str)
    oneFieldnot = []
    for field in searchStruct.oneFieldNotKeyWord.keys():
        str = "!"
        for key in searchStruct.oneFieldNotKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneFieldnot.append(str)
    return render(
        request, "searchresult.html", {
            "LegalDocList": legalDocuments[0:length:],
            "countResults": countResults,
            "resultCount": resultCount,
            "searchStruct": searchStruct,
            "onefield": oneField,
            "onefieldnot": oneFieldnot,
        })


@csrf_exempt
# 搜索结果页的重新搜索，java版本对应路径为“newsearch”
def newSearch(request):
    countResults.clear()
    global searchStruct
    searchStruct.clear()
    keyWord = request.POST.get('name')
    searchStruct = buildSearchStruct(keyWord)
    legalDocuments.clear()
    searchByStrcut(searchStruct)
    length = 10 if len(legalDocuments) > 10 else len(legalDocuments)

    oneField = []
    for field in searchStruct.oneFieldKeyWord.keys():
        str = ""
        for key in searchStruct.oneFieldKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneField.append(str)
    oneFieldnot = []
    for field in searchStruct.oneFieldNotKeyWord.keys():
        str = "!"
        for key in searchStruct.oneFieldNotKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneFieldnot.append(str)

    return render(
        request, "result.html", {
            "LegalDocList": legalDocuments[0:length:],
            "countResults": countResults,
            "resultCount": resultCount,
            "searchStruct": searchStruct,
            "onefield": oneField,
            "onefieldnot": oneFieldnot,
        })


@csrf_exempt
# 搜索结果页的结果内搜索，java版本对应路径为“addsearch”
def addSearch(request):
    queryString = request.POST.get('name')
    countResults.clear()
    legalDocuments.clear()
    buildSearchStruct(queryString)
    searchByStrcut(searchStruct)
    length = 10 if len(legalDocuments) > 10 else len(legalDocuments)
    # 生成用于产生标签的语句
    # print(searchStruct)
    oneField = []
    for field in searchStruct.oneFieldKeyWord.keys():
        str = ""
        for key in searchStruct.oneFieldKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneField.append(str)
    oneFieldnot = []
    for field in searchStruct.oneFieldNotKeyWord.keys():
        str = "!"
        for key in searchStruct.oneFieldNotKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneFieldnot.append(str)

    return render(
        request, "result.html", {
            "LegalDocList": legalDocuments[0:length:],
            "countResults": countResults,
            "resultCount": resultCount,
            "searchStruct": searchStruct,
            "onefield": oneField,
            "onefieldnot": oneFieldnot,
        })


@csrf_exempt
# 加载更多，java版本对应路径为getMore
def getMore(request):
    # 生成用于产生标签的语句
    oneField = []
    for field in searchStruct.oneFieldKeyWord.keys():
        str = ""
        for key in searchStruct.oneFieldKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneField.append(str)

    oneFieldnot = []
    for field in searchStruct.oneFieldNotKeyWord.keys():
        str = "!"
        for key in searchStruct.oneFieldNotKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneFieldnot.append(str)

    pageId = int(request.POST.get('name'))
    if pageId * 20 < len(legalDocuments):
        return render(
            request, "result.html", {
                "LegalDocList": legalDocuments[0:pageId * 20],
                "countResults": countResults,
                "resultCount": resultCount,
                "searchStruct": searchStruct,
                "onefield": oneField,
                "onefieldnot": oneFieldnot,
            })
    else:
        return render(
            request, "result.html", {
                "LegalDocList": legalDocuments[0:len(legalDocuments)],
                "countResults": countResults,
                "resultCount": resultCount,
                "searchStruct": searchStruct,
                "onefield": oneField,
                "onefieldnot": oneFieldnot,
            })

        # paginator = Paginator(legalDocuments, 10)
        # try:
        #     files = paginator.page(pageId)
        # except PageNotAnInteger:
        #     files = paginator.page(1)
        # except EmptyPage:
        #     files = paginator.page(paginator.num_pages)
        # return render(request, "result.html",
        #               {"LegalDocList": files, "countResults": countResults, "resultCount": resultCount})


@csrf_exempt
# 聚类搜索，java版本对应路径为addsearchandterm
def groupBySearch(request):
    legalDocuments.clear()
    countResults.clear()
    username = request.POST.get('name')
    keyword = username.split('@')[0].split(' ')
    if '@' in username:
        field = username.split('@')[1]
    else:
        field = "all"
    if field == "all":
        searchStruct.allFieldKeyWord = keyword
    else:
        searchStruct.oneFieldKeyWord.update({field: keyword})
    searchByStrcut(searchStruct)
    # print(searchStruct.oneFieldKeyWord.keys())
    oneField = []
    for field in searchStruct.oneFieldKeyWord.keys():
        str = ""
        for key in searchStruct.oneFieldKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneField.append(str)
    oneFieldnot = []
    for field in searchStruct.oneFieldNotKeyWord.keys():
        str = "!"
        for key in searchStruct.oneFieldNotKeyWord[field]:
            str = str + " " + key
        str = str + "@" + allSearchFieldListR[field]
        oneFieldnot.append(str)

    length = 10 if len(legalDocuments) > 10 else len(legalDocuments)

    return render(
        request, "result.html", {
            "LegalDocList": legalDocuments[0:length],
            "countResults": countResults,
            "resultCount": resultCount,
            "searchStruct": searchStruct,
            "onefield": oneField,
            "onefieldnot": oneFieldnot,
        })


@csrf_exempt
def getRecommond(request):
    es = Elasticsearch()
    if request.method == "POST":
        id=int(request.POST['id'])
        result=es.get(index='legal_index',
                doc_type='legalDocument',
                request_timeout=300,
                id=id)
        legalDocment = LegalDocument()
        legalDocment.id = result['_source']['id']
        legalDocment.fy = result['_source']['fy']
        legalDocment.dsrxx = result['_source']['dsrxx']
        legalDocment.ah = result['_source']['ah']
        legalDocment.spry = result['_source']['spry']
        legalDocment.ysfycm = result['_source']['ysfycm']
        legalDocment.ysqqqk = result['_source']['ysqqqk']
        legalDocment.byrw = result['_source']['byrw']
        legalDocment.spjg = result['_source']['spjg']
        legalDocment.ysdbqk = result['_source']['ysdbqk']
        legalDocment.esqqqk = result['_source']['esqqqk']
        legalDocment.ysfyrw = result['_source']['ysfyrw']
        legalDocment.ajms = result['_source']['ajms']
        legalDocment.xgft = result['_source']['xgft']
        legalDocment.sprq = result['_source']['sprq']
        legalDocment.sljg = result['_source']['sljg']
        legalDocment.bycm = result['_source']['bycm']
        legalDocment.sjy = result['_source']['sjy']
        legalDocment.bt = result['_source']['bt']
        legalDocment.wslx = result['_source']['wslx']
        legalDocment.dy = result['_source']['dy']
        legalDocment.nf = result['_source']['nf']
        legalDocment.slcx = result['_source']['slcx']
        legalDocment.ay = result['_source']['ay']
        legalDocment.ft = result['_source']['ft']
        legalDocment.tz = result['_source']['tz']
        legalDocment.fycj = result['_source']['fycj']
        # print(legalDocment.to_dict())
        return render(request, "resultDetail.html", {
        "legaldoc": legalDocment,
        "legalDocuments_id": legalDocment.id,

        })

@csrf_exempt
# 进入详细页面，java版本对应路径为searchresult
def getDetail(request):
    es = Elasticsearch()
    if request.method == "POST":
        legalDocuments_pos = int(request.POST["legalDocuments_id"])
        legalDocument = legalDocuments[legalDocuments_pos]
        print(legalDocument.id)

        return render(request, "resultDetail.html", {
            "legaldoc": legalDocument,
            "legalDocuments_id": legalDocuments_pos,
        })
    else:
        return render(request, "resultDetail.html")


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def getLegalDocument(legalDocument_id):
    es = Elasticsearch()
    result=es.get(index='legal_index',
                doc_type='legalDocument',
                request_timeout=300,
                id=legalDocument_id)
    legalDocment = LegalDocument()
    legalDocment.id = result['_source']['id']
    legalDocment.fy = result['_source']['fy']
    legalDocment.dsrxx = result['_source']['dsrxx']
    legalDocment.ah = result['_source']['ah']
    legalDocment.spry = result['_source']['spry']
    legalDocment.ysfycm = result['_source']['ysfycm']
    legalDocment.ysqqqk = result['_source']['ysqqqk']
    legalDocment.byrw = result['_source']['byrw']
    legalDocment.spjg = result['_source']['spjg']
    legalDocment.ysdbqk = result['_source']['ysdbqk']
    legalDocment.esqqqk = result['_source']['esqqqk']
    legalDocment.ysfyrw = result['_source']['ysfyrw']
    legalDocment.ajms = result['_source']['ajms']
    legalDocment.xgft = result['_source']['xgft']
    legalDocment.sprq = result['_source']['sprq']
    legalDocment.sljg = result['_source']['sljg']
    legalDocment.bycm = result['_source']['bycm']
    legalDocment.sjy = result['_source']['sjy']
    legalDocment.bt = result['_source']['bt']
    legalDocment.wslx = result['_source']['wslx']
    legalDocment.dy = result['_source']['dy']
    legalDocment.nf = result['_source']['nf']
    legalDocment.slcx = result['_source']['slcx']
    legalDocment.ay = result['_source']['ay']
    legalDocment.ft = result['_source']['ft']
    legalDocment.tz = result['_source']['tz']
    legalDocment.fycj = result['_source']['fycj']
    return legalDocment

##提供下载功能
@csrf_exempt
def download(request):
    # 没有登录
    if request.session['username'] == '':
        return render(request, 'account/login.html')
    if request.method == "POST":
        # legalDocuments_pos = int(request.POST["legalDocuments_id"])
        # legalDocument = legalDocuments[legalDocuments_pos]
        legalDocument = getLegalDocument(int(request.POST["legalDocumentId"]))
    # 临时文件名
    curr_date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    css = 'static/css/showDetail.css'
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    # path_wk = r'D:\wkhtmltopdf\bin\wkhtmltopdf.exe'  # 安装位置
    # config = pdfkit.configuration(wkhtmltopdf=path_wk)
    # 读文件并且替换动态内容
    # print(os.getcwd())
    fp = open(
        'static/download/pdf.html', 'w', encoding='utf-8')  # 打开你要写得文件test2.txt
    lines = open(
        'static/download/demo.html', 'r',
        encoding='utf-8').readlines()  # 打开文件，读入每一行
    for s in lines:
        # print(legalDocument.sljg)

        fp.write(
            s.replace('标题', '无' if not legalDocument.bt else legalDocument.bt)
            .replace('wenshuleixing', '无' if not legalDocument.wslx else legalDocument.wslx)
            .replace('nianfen', '无' if not legalDocument.nf else legalDocument.nf)
            .replace('shenlichengxu', '无' if not legalDocument.slcx else legalDocument.slcx)
            .replace('fayuancengji', '无' if not legalDocument.fycj else legalDocument.fycj)
            .replace('diyu', '无' if not legalDocument.dy else legalDocument.dy)
            .replace('anhao', '无' if not legalDocument.ah else legalDocument.ah)
            .replace('dangshirenxingxi', '无' if not legalDocument.dsrxx else legalDocument.dsrxx)
            .replace('anjianmiaoshu', '无' if not legalDocument.ajms else legalDocument.ajms)
            .replace('shenlijingguo', '无' if not legalDocument.sljg else legalDocument.sljg)
            .replace('yishenqingqiuqingkuang', '无' if not legalDocument.ysqqqk else legalDocument.ysqqqk)
            .replace('yishendabianqingkuang', '无' if not legalDocument.ysdbqk else legalDocument.ysdbqk)
            .replace('yishenfayuanchaming', '无' if not legalDocument.ysfycm else legalDocument.ysfycm)
            .replace('yishenfayuanrenwei', '无' if not legalDocument.ysfyrw else legalDocument.ysfyrw)
            .replace('ershenqingqiuqingkuang', '无' if not legalDocument.esqqqk else legalDocument.esqqqk)
            .replace('benyuanchaming', '无' if not legalDocument.bycm else legalDocument.bycm)
            .replace('benyuanrenwei', '无' if not legalDocument.byrw else legalDocument.byrw)
            .replace('shenpanjieguo', '无' if not legalDocument.spjg else legalDocument.spjg)
            .replace('shenpanrenyuan', '无' if not legalDocument.spry else legalDocument.spry)
            .replace('shenpanriqi', '无' if not legalDocument.sprq else legalDocument.sprq)
            .replace('shujiyuan', '无' if not legalDocument.sjy else legalDocument.sjy)
            .replace('xiangguanfatiao', '无' if not legalDocument.xgft else legalDocument.xgft)
            )

        # replace是替换，write是写入

    fp.close()  # 关闭文件
    outpath = 'static/download/out%s.pdf' % (curr_date)
    pdfkit.from_file(
        'static/download/pdf.html',
        options=options,
        css=css,
        output_path=outpath)
    # configuration=config)
    # 文件下载
    file = open(r'%s' % (outpath), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (outpath)
    return response


@csrf_exempt
def getRecommondList(request):
    es = Elasticsearch()

    id = int(request.POST['id'])
    result = es.get(index='legal_index',
                        doc_type='legalDocument',
                        request_timeout=300,
                        id=id)
    legalDocment = LegalDocument()
    legalDocment.id = result['_source']['id']
    legalDocment.fy = result['_source']['fy']
    legalDocment.dsrxx = result['_source']['dsrxx']
    legalDocment.ah = result['_source']['ah']
    legalDocment.spry = result['_source']['spry']
    legalDocment.ysfycm = result['_source']['ysfycm']
    legalDocment.ysqqqk = result['_source']['ysqqqk']
    legalDocment.byrw = result['_source']['byrw']
    legalDocment.spjg = result['_source']['spjg']
    legalDocment.ysdbqk = result['_source']['ysdbqk']
    legalDocment.esqqqk = result['_source']['esqqqk']
    legalDocment.ysfyrw = result['_source']['ysfyrw']
    legalDocment.ajms = result['_source']['ajms']
    legalDocment.xgft = result['_source']['xgft']
    legalDocment.sprq = result['_source']['sprq']
    legalDocment.sljg = result['_source']['sljg']
    legalDocment.bycm = result['_source']['bycm']
    legalDocment.sjy = result['_source']['sjy']
    legalDocment.bt = result['_source']['bt']
    legalDocment.wslx = result['_source']['wslx']
    legalDocment.dy = result['_source']['dy']
    legalDocment.nf = result['_source']['nf']
    legalDocment.slcx = result['_source']['slcx']
    legalDocment.ay = result['_source']['ay']
    legalDocment.ft = result['_source']['ft']
    legalDocment.tz = result['_source']['tz']
    legalDocment.fycj = result['_source']['fycj']
    recommendCounts = getRecommondDetail(legalDocment)
    print('返回')
    print(recommendCounts)
    ids = recommendCounts.keys()
    legaldoclist = []
    for id in ids:
        result = es.get(
            index='legal_index',
            doc_type='legalDocument',
            request_timeout=300,
            id=id)
        legalDoc = LegalDocument()
        legalDoc.id = result['_source']['id']
        legalDoc.similarity=recommendCounts.get(id)
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
        legalDoc.ajms = result['_source']['ajms']
        legalDoc.xgft = result['_source']['xgft']
        legalDoc.sprq = result['_source']['sprq']
        legalDoc.sljg = result['_source']['sljg']
        legalDoc.bycm = result['_source']['bycm']
        legalDoc.sjy = result['_source']['sjy']
        legalDoc.bt = result['_source']['bt']
        legalDoc.wslx = result['_source']['wslx']
        legalDoc.dy = result['_source']['dy']
        legalDoc.nf = result['_source']['nf']
        legalDoc.slcx = result['_source']['slcx']
        legalDoc.ay = result['_source']['ay']
        legalDoc.ft = result['_source']['ft']
        legalDoc.tz = result['_source']['tz']
        legalDoc.fycj = result['_source']['fycj']
        legaldoclist.append(legalDoc)
        # print(legaldoclist)

    print(legaldoclist)
    return render(request, "recommond.html", {

             "legaldoclist": legaldoclist
     })


# 进入推荐页面，java版本对应路径为recommondDetail
def getRecommondDetail(legalDocument):
    fileResults = os.path.join(r'/home/mianhuatang/提取','')
    print(gc.collect())
    id=legalDocument.id
    es = Elasticsearch()
    searchResult = es.get(
        index='legal_index',
        doc_type='legalDocument',
        request_timeout=300,
        id=id)
    ay=searchResult['_source']['ay'].split('\t')[0:2]
    ayLen=len(ay)
    recommendResult={}
    for i in range(len(ay)):
        if(ay[i]=='' or ay[i] in exceptionAY ):
            continue
        anyou=ay[i]
        print(anyou + " " + str(gc.collect()))
        searchResult=es.get(index='legal_keywords',doc_type='keyword',request_timeout=300,id=id)
        keywords=searchResult['_source']['keywords'].split('\t')
        # 分词文件路径
        filepath = os.path.join('/home/mianhuatang/提取', anyou)
        # 到该案由路径下载入获取已经训练好的模型
        output = os.path.join('/home/mianhuatang/data/results', anyou)

        # 载入字典
        dictionary = corpora.Dictionary.load(os.path.join(output, "all.dic"))

        # # 载入LDA模型和索引
        ldaModel = models.LdaModel.load(os.path.join(output, "allLDATopic.mdl"))
        indexLDA = similarities.MatrixSimilarity.load(os.path.join(output, "allLDATopic.idx"))

        # query就是测试数据，先切词
        query_bow = dictionary.doc2bow(keywords)

        # 载入TFIDF模型和索引
        tfidfModel = models.TfidfModel.load(os.path.join(output, "allTFIDF.mdl"))
        indexTfidf = similarities.MatrixSimilarity.load(os.path.join(output, "allTFIDF.idx"))

        # 使用TFIDF模型向量化
        tfidfvect = tfidfModel[query_bow]

        # 然后LDA向量化，因为我们训练时的LDA是在TFIDF基础上做的，所以用itidfvect再向量化一次
        ldavec = ldaModel[tfidfvect]

        # TFIDF相似性，相似性列表记录与每份模型中的文书的相似度
        simstfidf = indexTfidf[tfidfvect]

        # LDA相似性，相似性列表记录与每份模型中的文书的相似度
        simlda = indexLDA[ldavec]

        sort_sims = sorted(enumerate(simlda), key=lambda item: -item[1])

        ldaNumber = {}
        for keys in sort_sims[0:11]:
            key = keys[0]
            key = str(key)
            while len(key) < 8:
                key = "0" + key
            key = key + '.txt'
            file = open(os.path.join(filepath, key), encoding='UTF-8')
            lines = file.readlines()
            for line in lines:  # 将文件中的编号装入列表
                if len(line) != 1:
                    if line.split('##')[0] == '编号':
                        ldaNumber[line.split('##')[1].strip('\n')] = keys[1]
        recommendResult.update(ldaNumber)

    print('排序前')
    print(recommendResult)
    sorted(recommendResult.items(), key=lambda d: d[1],reverse=True)

    resultKeys=recommendResult.keys()
    recommendResults={}
    i=0
    for key in resultKeys :
        if int(key)!=id and i<11:
            recommendResults[key]=recommendResult.get(key)
            i=i+1

    print(gc.collect())
    print('排序后')
    print(recommendResults.items())
    return recommendResults


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

    allFieldKeyWordQuery = {"bool": {"must": allFieldKeyWordQuery}}

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

    allFieldNotKeyWordQuery = {"bool": {"must": allFieldNotKeyWordQuery}}

    return allFieldNotKeyWordQuery


# 单领域搜索
def oneFieldSearch(searchStruct):
    oneFieldKeyWordQuery = []
    oneFieldKeyWordMiniQuery = []
    if searchStruct.oneFieldKeyWord:
        oneFieldKeyWord = searchStruct.oneFieldKeyWord
        # oneFieldKeyWord = {"byrw" :["盗窃", "窃取"], "bt": ["盗窃"]}
        fieldSet = oneFieldKeyWord.keys()
        for field in fieldSet:
            for keyWord in oneFieldKeyWord[field]:
                oneFieldKeyWordMiniQuery.append({
                    "match_phrase": {
                        field: keyWord
                    }
                })
            oneFieldKeyWordQuery.append({
                "bool": {
                    "must": oneFieldKeyWordMiniQuery
                }
            })
            oneFieldKeyWordMiniQuery = []

    oneFieldKeyWordQuery = {"bool": {"must": oneFieldKeyWordQuery}}

    return oneFieldKeyWordQuery


# 单领域否定搜索:输出：oneFieldKeyNotWordQuery
def oneFieldNotSearch(searchStruct):
    oneFieldKeyNotWordQuery = []
    oneFieldKeyNotWordMiniQuery = []
    if searchStruct.oneFieldNotKeyWord:
        oneFieldNotKeyWord = searchStruct.oneFieldNotKeyWord
        fieldSet = oneFieldNotKeyWord.keys()
        for field in fieldSet:
            for keyWord in oneFieldNotKeyWord[field]:
                oneFieldKeyNotWordMiniQuery.append({
                    "match_phrase": {
                        field: keyWord
                    }
                })
            oneFieldKeyNotWordQuery = ({
                "bool": {
                    "must_not": oneFieldKeyNotWordMiniQuery
                }
            })
            oneFieldKeyNotWordMiniQuery = []
    oneFieldKeyNotWordQuery = {"bool": {"must": oneFieldKeyNotWordQuery}}
    return oneFieldKeyNotWordQuery


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
        fieldKeyWordQueryCopy = fieldKeyWordQuery
        fieldKeyWordQuery = {"bool": {"should": fieldKeyWordQueryCopy}}

    fieldKeyWordQuery = {"bool": {"must": fieldKeyWordQuery}}

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

    orderFieldKeyWordQuery = {"bool": {"must": orderFieldKeyWordQuery}}

    return orderFieldKeyWordQuery


#对于聚合结果进行排序
def sortGroupByResults(countResult):
    temp = {}
    for i in countResult:
        temp[i['key']] = i['doc_count']
    sortKeys = sorted(temp.keys())
    result = []
    for i in sortKeys:
        result.append({'key': i, 'doc_count': temp[i]})
    return result


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

        "size": 1000,
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
            "wslx": {
                "terms": {
                    "field": "wslx"
                }
            },
            "nf": {
                "terms": {
                    "field": "nf"
                }
            },
            "ay": {
                "terms": {
                    "field": "ay"
                }
            },
            "dy": {
                "terms": {
                    "field": "dy"
                }
            },
            "slcx": {
                "terms": {
                    "field": "slcx"
                }
            }
        },
        "highlight": {
            "require_field_match": True,
            "fields": {
                "fy": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "dsrxx": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "ah": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "spry": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "ysfycm": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "ysqqqk": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "byrw": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "spjg": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "ysdbqk": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "esqqqk": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "ysfyrw": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "wslx": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "ajms": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "xgft": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "sprq": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "sljg": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "bycm": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "sjy": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                },
                "bt": {
                    "pre_tags": "<span style=\"color:red\">",
                    "post_tags": "</span>",
                    "number_of_fragments": 0
                }
            }
        }
    }

    # print(json.dumps(query))
    searchResults = es.search(
        index='legal_index',
        doc_type='legalDocument',
        request_timeout=300,
        body=json.dumps(query))

    global resultCount
    resultCount = searchResults['hits']['total']
    results = searchResults['hits']['hits']

    countResults['dy'] = searchResults['aggregations']['dy']['buckets']
    countResults['nf'] = sortGroupByResults(
        searchResults['aggregations']['nf']['buckets'])

    countResults['ay'] = searchResults['aggregations']['ay']['buckets']
    countResults['fycj'] = searchResults['aggregations']['fycj']['buckets']
    countResults['slcx'] = searchResults['aggregations']['slcx']['buckets']
    countResults['wslx'] = searchResults['aggregations']['wslx']['buckets']

    for result in results:
        legalDoc = LegalDocument()
        legalDoc.id=result['_source']['id']
        if ('highlight' in result and result['highlight'].__contains__('fy')):
            legalDoc.fy = result['highlight']['fy'][0]
        else:
            legalDoc.fy = result['_source']['fy']

        if ('highlight' in result
                and result['highlight'].__contains__('dsrxx')):
            legalDoc.dsrxx = result['highlight']['dsrxx'][0]
        else:
            legalDoc.dsrxx = result['_source']['dsrxx']

        if ('highlight' in result and result['highlight'].__contains__('ah')):
            legalDoc.ah = result['highlight']['ah'][0]
        else:
            legalDoc.ah = result['_source']['ah']

        if ('highlight' in result
                and result['highlight'].__contains__('spry')):
            legalDoc.spry = result['highlight']['spry'][0]
        else:
            legalDoc.spry = result['_source']['spry']

        if ('highlight' in result
                and result['highlight'].__contains__('ysfycm')):
            legalDoc.ysfycm = result['highlight']['ysfycm'][0]
        else:
            legalDoc.ysfycm = result['_source']['ysfycm']

        if ('highlight' in result
                and result['highlight'].__contains__('ysqqqk')):
            legalDoc.ysqqqk = result['highlight']['ysqqqk'][0]
        else:
            legalDoc.ysqqqk = result['_source']['ysqqqk']

        if ('highlight' in result
                and result['highlight'].__contains__('byrw')):
            legalDoc.byrw = result['highlight']['byrw'][0]
        else:
            legalDoc.byrw = result['_source']['byrw']

        if ('highlight' in result
                and result['highlight'].__contains__('spjg')):
            legalDoc.spjg = result['highlight']['spjg'][0]
        else:
            legalDoc.spjg = result['_source']['spjg']

        if ('highlight' in result
                and result['highlight'].__contains__('ysdbqk')):
            legalDoc.ysdbqk = result['highlight']['ysdbqk'][0]
        else:
            legalDoc.ysdbqk = result['_source']['ysdbqk']

        if ('highlight' in result
                and result['highlight'].__contains__('esqqqk')):
            legalDoc.esqqqk = result['highlight']['esqqqk'][0]
        else:
            legalDoc.esqqqk = result['_source']['esqqqk']

        if ('highlight' in result
                and result['highlight'].__contains__('ysfyrw')):
            legalDoc.ysfyrw = result['highlight']['ysfyrw'][0]
        else:
            legalDoc.ysfyrw = result['_source']['ysfyrw']

        if ('highlight' in result
                and result['highlight'].__contains__('ajms')):
            legalDoc.ajms = result['highlight']['ajms'][0]
        else:
            legalDoc.ajms = result['_source']['ajms']

        if ('highlight' in result
                and result['highlight'].__contains__('xgft')):
            legalDoc.xgft = result['highlight']['xgft'][0]
        else:
            legalDoc.xgft = result['_source']['xgft']

        if ('highlight' in result
                and result['highlight'].__contains__('sprq')):
            legalDoc.sprq = result['highlight']['sprq'][0]
        else:
            legalDoc.sprq = result['_source']['sprq']

        if ('highlight' in result
                and result['highlight'].__contains__('sljg')):
            legalDoc.sljg = result['highlight']['sljg'][0]
        else:
            legalDoc.sljg = result['_source']['sljg']

        if ('highlight' in result
                and result['highlight'].__contains__('bycm')):
            legalDoc.bycm = result['highlight']['bycm'][0]
        else:
            legalDoc.bycm = result['_source']['bycm']

        if ('highlight' in result and result['highlight'].__contains__('sjy')):
            legalDoc.sjy = result['highlight']['sjy'][0]
        else:
            legalDoc.sjy = result['_source']['sjy']

        if ('highlight' in result and result['highlight'].__contains__('bt')):
            legalDoc.bt = result['highlight']['bt'][0]
        else:
            legalDoc.bt = result['_source']['bt']

        legalDoc.wslx = result['_source']['wslx']

        legalDoc.dy = result['_source']['dy']
        legalDoc.nf = result['_source']['nf']
        legalDoc.slcx = result['_source']['slcx']
        legalDoc.ay = result['_source']['ay']
        legalDoc.ft = result['_source']['ft']
        legalDoc.tz = result['_source']['tz']
        legalDoc.fycj = result['_source']['fycj']
        legalDocuments.append(legalDoc)

    return legalDocuments, countResults
