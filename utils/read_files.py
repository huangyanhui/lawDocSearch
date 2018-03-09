import time
import os
import re
import shutil
from elastic_search import ElasticSearchUtils
from lawDoc.models import LegalDocument

# 设置根目录
root_path = ''
basic_info_path = '刑事案件/文书基本信息'
info_path = '刑事案件/法律文书'


def get_folder_list(path):
    return os.listdir(path)


def move_9999():
    for sub_dir in get_folder_list(root_path):
        provinces = get_folder_list(root_path + '/' + sub_dir)
        for province in provinces:
            if province == '9999':
                shutil.move(
                    root_path + '/' + sub_dir + '/' + province,
                    root_path + '/' + sub_dir + '/' + '江苏' + '/' + province)


def regax_replace(s, rule):
    compiler = re.compile(rule)
    s = compiler.sub('', s)
    return s


def replace_html_special_character(s):
    return regax_replace(s, u'&[a-zA-Z0-9]+;')


def keep_chinese_english_and_number(s):
    return regax_replace(s, u'[^\u4e00-\u9fa5a-zA-Z0-9-，。、；！：（）”“《》？]')


def text_decoration(s):
    return keep_chinese_english_and_number(replace_html_special_character(s))


def file_split(f, sign='##'):
    res = {}
    for line in f.readlines():
        s = line.split(sign)
        keyword = text_decoration(s[0])
        content = text_decoration(s[1])
        if keyword in res:
            if keyword == '审判人员':
                res[keyword] += '\n' + content
            elif keyword == '引用法条':
                res[keyword] += '\t' + content
            else:
                res[keyword] += content
        else:
            res[keyword] = content
    return res


def generate_feature(d, keywords):
    feature = set()
    for v in d.values():
        for k in keywords:
            if k in v:
                feature.add(k)

    return '\t'.join(list(feature))


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


def wrapper(id, basic, content, provider):
    limit = 4096
    legal_doc = LegalDocument()
    legal_doc.id = id
    legal_doc.fy = has_key(content, '法院')
    legal_doc.dsrxx = has_key(content, '当事人信息')
    legal_doc.dsrxxcopy = has_key(content, '当事人信息')[:limit]
    legal_doc.ah = has_key(content, '案号')
    legal_doc.ahcopy = has_key(content, '案号')[:limit]
    legal_doc.spry = has_key(content, '审判人员')
    legal_doc.sprycopy = has_key(content, '审判人员')[:limit]
    legal_doc.ysfycm = has_key(content, '一审法院查明')
    legal_doc.ysfycmcopy = has_key(content, '一审法院查明')[:limit]
    legal_doc.ysfycmcopy2 = has_key(content, '一审法院查明')[limit:limit * 2]
    legal_doc.ysqqqk = has_key(content, '一审请求情况')
    legal_doc.ysqqqkcopy = has_key(content, '一审请求情况')[:limit]
    legal_doc.ysqqqkcopy2 = has_key(content, '一审请求情况')[limit:limit * 2]
    legal_doc.byrw = has_key(content, '本院认为')
    legal_doc.byrwcopy = has_key(content, '本院认为')[:limit]
    legal_doc.byrwcopy2 = has_key(content, '本院认为')[limit:limit * 2]
    legal_doc.spjg = has_key(content, '审判结果')
    legal_doc.spjgcopy = has_key(content, '审判结果')[:limit]
    legal_doc.spjgcopy2 = has_key(content, '审判结果')[limit:limit * 2]
    legal_doc.ysdbqk = has_key(content, '一审答辩情况')
    legal_doc.ysdbqkcopy = has_key(content, '一审答辩情况')[:limit]
    legal_doc.ysdbqkcopy2 = has_key(content, '一审答辩情况')[limit:limit * 2]
    legal_doc.esqqqk = has_key(content, '二审请求情况')
    legal_doc.esqqqkcopy = has_key(content, '二审请求情况')[:limit]
    legal_doc.esqqqkcopy2 = has_key(content, '二审请求情况')[limit:limit * 2]
    legal_doc.ysfyrw = has_key(content, '一审法院认为')
    legal_doc.ysfyrwcopy = has_key(content, '一审法院认为')[:limit]
    legal_doc.ysfyrwcopy2 = has_key(content, '一审法院认为')[limit:limit * 2]
    legal_doc.wslx = document_type(has_key(content, '文书类型'))
    legal_doc.ajms = has_key(content, '案例描述')
    legal_doc.ajmscopy = has_key(content, '案例描述')[:limit]
    legal_doc.ajmscopy2 = has_key(content, '案例描述')[limit:limit * 2]
    legal_doc.xgft = has_key(content, '相关法条')
    legal_doc.xgftcopy = has_key(content, '相关法条')[:limit]
    legal_doc.sprq = has_key(content, '审判日期')
    legal_doc.sprqcopy = has_key(content, '审判日期')[:limit]
    legal_doc.sljg = has_key(content, '审理经过')
    legal_doc.sljgcopy = has_key(content, '审理经过')[:limit]
    legal_doc.sljgcopy2 = has_key(content, '审理经过')[limit:limit * 2]
    legal_doc.bycm = has_key(content, '本院查明')
    legal_doc.bycmcopy = has_key(content, '本院查明')[:limit]
    legal_doc.bycmcopy2 = has_key(content, '本院查明')[limit:limit * 2]
    legal_doc.sjy = has_key(content, '书记员')
    legal_doc.sjycopy2 = has_key(content, '书记员')[:limit]
    legal_doc.bt = has_key(content, '标题')
    legal_doc.btcopy = has_key(content, '标题')[:limit]
    legal_doc.fycj = court_level(has_key(content, '法院'))
    legal_doc.dy = provider
    # legal_doc.nf = has_key(basic, '日期')[:4]
    legal_doc.nf = get_year(basic)
    legal_doc.slcx = has_key(basic, '审理程序')
    legal_doc.ay = has_key(basic, '案由')
    legal_doc.ft = has_key(basic, '引用法条')
    legal_doc.tz = has_key(content, '特征')

    return legal_doc


def main():
    id_generator = 0
    es_utils = ElasticSearchUtils()
    legal_docs = []

    keywords = []
    # 设置关键词文本路径
    keywords_file = open('刑事/刑事文书分段结果/关键词.txt', 'r')
    for line in keywords_file.readlines():
        s = re.sub('\s', '', line)
        keywords.append(s)

    for sub_dir in get_folder_list(root_path):
        provinces = get_folder_list(root_path + '/' + sub_dir)
        for province in provinces:
            folder_ids = get_folder_list(
                root_path + '/' + sub_dir + '/' + province)
            for folder_id in folder_ids:
                file_list = get_folder_list(
                    root_path + '/' + sub_dir + '/' + province + '/' +
                    folder_id + '/' + basic_info_path)
                for f in file_list:
                    id_generator += 1
                    basic_file = open(
                        root_path + '/' + sub_dir + '/' + province + '/' +
                        folder_id + '/' + basic_info_path + '/' + f, 'r')
                    basic_dict = file_split(basic_file)
                    content_file = open(
                        root_path + '/' + sub_dir + '/' + province + '/' +
                        folder_id + '/' + info_path + '/' + f, 'r')
                    content_dict = file_split(content_file)
                    content_dict['特征'] = generate_feature(
                        content_dict, keywords)

                    legal_docs.append(
                        wrapper(id_generator, basic_dict, content_dict,
                                province))

                    if id_generator % 10000 == 0:
                        print(
                            time.strftime('%Y-%m-%d %H:%M',
                                          time.localtime(time.time())))
                        print(id_generator)
                        es_utils.add_data_bulk(legal_docs, bulk_num=10000)
                        del legal_docs[0:len(legal_docs)]
                        time.sleep(5)

    if len(legal_docs) > 0:
        print(time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))
        print(id_generator)
        es_utils.add_data_bulk(legal_docs, bulk_num=10000)
        del legal_docs[0:len(legal_docs)]


if __name__ == '__main__':
    main()
