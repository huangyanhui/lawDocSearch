from lawDoc.models import LegalDocument

import re


def is_validate_year(year):
    return 1900 < year and year <= 2017


def convert_to_int(s):
    try:
        return int(s)
    except ValueError:
        return 2048


def get_year(d):
    if has_key(d, '日期') != '' and is_validate_year(
            convert_to_int(d['日期'][:4])):
        return d['日期'][:4]
    elif has_key(d, '案号') != '':
        s = re.sub(r'[^0-9]', '', d['案号'])[:4]
        if is_validate_year(convert_to_int(s)):
            return s
    else:
        return '2048'


def court_level(s):
    if s.find('最高') != -1:
        return '最高人民法院'
    elif s.find('高级') != -1:
        return '高级人民法院'
    elif s.find('中级') != -1:
        return '中级人民法院'
    else:
        return '基层人民法院'


def document_type(s):
    type_list = set(['刑事裁定书', '刑事判决书', '刑事附带民事判决书', '刑事附带民事裁定书', '强制医疗决定书'])
    if s in type_list:
        return s
    elif s.find('判决书') != -1:
        return '刑事判决书'
    else:
        return '刑事裁定书'


def has_key(d, key):
    if key in d:
        return d[key]
    else:
        return ''


def wrapper(id, d):
    '''
    把字典转化为 LegalDocument

    d: 传入字典
    limit: 字符串长度限制
    '''
    limit = 4096
    legal_doc = LegalDocument()
    legal_doc.id = id
    legal_doc.fy = has_key(d, '法院')
    legal_doc.dsrxx = has_key(d, '当事人信息')
    legal_doc.dsrxxcopy = has_key(d, '当事人信息')[:limit]
    legal_doc.ah = has_key(d, '案号')
    legal_doc.ahcopy = has_key(d, '案号')[:limit]
    legal_doc.spry = has_key(d, '审判人员')
    legal_doc.sprycopy = has_key(d, '审判人员')[:limit]
    legal_doc.ysfycm = has_key(d, '一审法院查明')
    legal_doc.ysfycmcopy = has_key(d, '一审法院查明')[:limit]
    legal_doc.ysfycmcopy2 = has_key(d, '一审法院查明')[limit:limit * 2]
    legal_doc.ysqqqk = has_key(d, '一审请求情况')
    legal_doc.ysqqqkcopy = has_key(d, '一审请求情况')[:limit]
    legal_doc.ysqqqkcopy2 = has_key(d, '一审请求情况')[limit:limit * 2]
    legal_doc.byrw = has_key(d, '本院认为')
    legal_doc.byrwcopy = has_key(d, '本院认为')[:limit]
    legal_doc.byrwcopy2 = has_key(d, '本院认为')[limit:limit * 2]
    legal_doc.spjg = has_key(d, '审判结果')
    legal_doc.spjgcopy = has_key(d, '审判结果')[:limit]
    legal_doc.spjgcopy2 = has_key(d, '审判结果')[limit:limit * 2]
    legal_doc.ysdbqk = has_key(d, '一审答辩情况')
    legal_doc.ysdbqkcopy = has_key(d, '一审答辩情况')[:limit]
    legal_doc.ysdbqkcopy2 = has_key(d, '一审答辩情况')[limit:limit * 2]
    legal_doc.esqqqk = has_key(d, '二审请求情况')
    legal_doc.esqqqkcopy = has_key(d, '二审请求情况')[:limit]
    legal_doc.esqqqkcopy2 = has_key(d, '二审请求情况')[limit:limit * 2]
    legal_doc.ysfyrw = has_key(d, '一审法院认为')
    legal_doc.ysfyrwcopy = has_key(d, '一审法院认为')[:limit]
    legal_doc.ysfyrwcopy2 = has_key(d, '一审法院认为')[limit:limit * 2]
    legal_doc.wslx = document_type(has_key(d, '文书类型'))
    legal_doc.ajms = has_key(d, '案例描述')
    legal_doc.ajmscopy = has_key(d, '案例描述')[:limit]
    legal_doc.ajmscopy2 = has_key(d, '案例描述')[limit:limit * 2]
    legal_doc.xgft = has_key(d, '相关法条')
    legal_doc.xgftcopy = has_key(d, '相关法条')[:limit]
    legal_doc.sprq = has_key(d, '审判日期')
    legal_doc.sprqcopy = has_key(d, '审判日期')[:limit]
    legal_doc.sljg = has_key(d, '审理经过')
    legal_doc.sljgcopy = has_key(d, '审理经过')[:limit]
    legal_doc.sljgcopy2 = has_key(d, '审理经过')[limit:limit * 2]
    legal_doc.bycm = has_key(d, '本院查明')
    legal_doc.bycmcopy = has_key(d, '本院查明')[:limit]
    legal_doc.bycmcopy2 = has_key(d, '本院查明')[limit:limit * 2]
    legal_doc.sjy = has_key(d, '书记员')
    legal_doc.sjycopy2 = has_key(d, '书记员')[:limit]
    legal_doc.bt = has_key(d, '标题')
    legal_doc.btcopy = has_key(d, '标题')[:limit]
    legal_doc.fycj = court_level(has_key(d, '法院'))
    legal_doc.dy = has_key(d, '省份')
    legal_doc.nf = get_year(d)
    legal_doc.slcx = has_key(d, '审理程序')
    legal_doc.ay = has_key(d, '案由')
    legal_doc.ft = has_key(d, '引用法条')
    legal_doc.tz = has_key(d, '特征')

    return legal_doc
