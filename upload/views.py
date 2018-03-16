from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from utils.elastic_search import ElasticSearchUtils
from utils.text_process import text_decoration
from utils.wrapper import wrapper

import json


@csrf_exempt
def upload(request):
    # DEBUG 语句
    # request.session['identity'] = 2
    # DEBUG 语句
    # 普通用户直接返回主页
    if request.session['identity'] == 1:
        return render(
            request, 'index.html', {
                'username': request.session['username'],
                'allowed_count': request.session['allowed_count']
            })
    else:
        if request.method == 'POST':
            response = {}
            response['operation'] = 'upload'
            original_text = request.POST.get('orignal-text')
            split_sign = '##'
            if request.POST.get('split-sign') == '':
                split_sign = '##'
            else:
                split_sign = request.POST.get('split-sign')
                original_dict = text_split(original_text, sign=split_sign)
                # 如果存在与数据库中
                if is_in_database(original_dict['案号']):
                    response['status'] = 'failed'
                    response['message'] = 'exists'
                # 不在数据库时上传
                else:
                    es_utils = ElasticSearchUtils()
                    new_id = get_total() + 1
                    new_legal_doc = wrapper(new_id, original_dict)
                    es_utils.add_data(new_legal_doc)
                    response['status'] = 'success'

            return HttpResponse(json.dumps(response, ensure_ascii=False))
        # 跳转到上传页面
        else:
            return render(request, 'upload/index.html')


def text_split(text, sign='##'):
    res = {}
    original_split = text.split('\n')
    for line in original_split:
        if line != '':
            s = line.split(sign)
            keyword = text_decoration(s[0])
            content = text_decoration(s[1])
            if keyword in res:
                if keyword == '审判人员':
                    res[keyword] += '\n' + content
                elif keyword == '引用法条':
                    res[keyword] += '\t' + content
                elif keyword == '案号':
                    continue
                else:
                    res[keyword] += content
            else:
                res[keyword] = content
    return res


def is_in_database(ah):
    '''
    是否存在数据库

    ah: 案号
    '''
    print(ah)
    es_utils = ElasticSearchUtils()
    body = {'query': {'bool': {'must': {'match_phrase': {'ah': ah}}}}}
    res = es_utils.search(body)
    # 此案号存在与数据库
    if res['hits']['total'] > 0:
        return True
    else:
        return False


def get_total():
    es_utils = ElasticSearchUtils()
    body = {'query': {'match_all': {}}}
    res = es_utils.search(body)
    return int(res['hits']['total'])
