import re


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
