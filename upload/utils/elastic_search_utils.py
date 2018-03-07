from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
# from lawDoc.models import LegalDocument
from os import environ

import json


class LegalDocument():
    # 构造函数,id,法院，当事人信息，案号，审判人员，一审法院查明
    def __init__(self):
        # id
        self.id = 0
        # 法院
        self.fy = ''
        # 当事人信息
        self.dsrxx = ''
        self.dsrxxcopy = ''
        # 案号
        self.ah = ''
        self.ahcopy = ''
        # 审判人员
        self.spry = ''
        self.sprycopy = ''
        # 一审法院查明
        self.ysfycm = ''
        self.ysfycmcopy = ''
        self.ysfycmcopy2 = ''
        # 一审请求情况
        self.ysqqqk = ''
        self.ysqqqkcopy = ''
        self.ysqqqkcopy2 = ''
        # 本院认为
        self.byrw = ''
        self.byrwcopy = ''
        self.byrwcopy2 = ''
        # 审判结果
        self.spjg = ''
        self.spjgcopy = ''
        self.spjgcopy2 = ''
        # 一审答辩情况
        self.ysdbqk = ''
        self.ysdbqkcopy = ''
        self.ysdbqkcopy2 = ''
        # 二审请求情况
        self.esqqqk = ''
        self.esqqqkcopy = ''
        self.esqqqkcopy2 = ''
        # 一审法院认为
        self.ysfyrw = ''
        self.ysfyrwcopy = ''
        self.ysfyrwcopy2 = ''
        # 文书类型
        self.wslx = ''
        # 案例描述
        self.ajms = ''
        self.ajmscopy = ''
        self.ajmscopy2 = ''
        # 相关法条
        self.xgft = ''
        self.xgftcopy = ''
        # 审判日期
        self.sprq = ''
        self.sprqcopy = ''
        # 审理经过
        self.sljg = ''
        self.sljgcopy = ''
        self.sljgcopy2 = ''
        # 本院查明
        self.bycm = ''
        self.bycmcopy = ''
        self.bycmcopy2 = ''
        # 书记员
        self.sjy = ''
        self.sjycopy2 = ''
        # 标题
        self.bt = ''
        self.btcopy = ''
        # 法院层级
        self.fycj = ''
        # 地域
        self.dy = ''
        # 年份
        self.nf = ''
        # 审理程序
        self.slcx = ''
        # 案由
        self.ay = ''
        # 法条
        self.ft = ''
        # 特征
        self.tz = ''

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def to_dict(self):
        return {
            'id': self.id,
            'fy': self.fy,
            'dsrxx': self.dsrxx,
            'dsrxxcopy': self.dsrxxcopy,
            'ah': self.ah,
            'ahcopy': self.ahcopy,
            'spry': self.spry,
            'sprycopy': self.sprycopy,
            'ysfycm': self.ysfycm,
            'ysfycmcopy': self.ysfycmcopy,
            'ysfycmcopy2': self.ysfycmcopy2,
            'ysqqqk': self.ysqqqk,
            'ysqqqkcopy': self.ysqqqkcopy,
            'ysqqqkcopy2': self.ysqqqkcopy2,
            'byrw': self.byrw,
            'byrwcopy': self.byrwcopy,
            'byrwcopy2': self.byrwcopy2,
            'spjg': self.spjg,
            'spjgcopy': self.spjgcopy,
            'spjgcopy2': self.spjgcopy2,
            'ysdbqk': self.ysdbqk,
            'ysdbqkcopy': self.ysdbqkcopy,
            'ysdbqkcopy2': self.ysdbqkcopy2,
            'esqqqk': self.esqqqk,
            'esqqqkcopy': self.esqqqkcopy,
            'esqqqkcopy2': self.esqqqkcopy2,
            'ysfyrw': self.ysfyrw,
            'ysfyrwcopy': self.ysfyrwcopy,
            'ysfyrwcopy2': self.ysfyrwcopy2,
            'wslx': self.wslx,
            'ajms': self.ajms,
            'ajmscopy': self.ajmscopy,
            'ajmscopy2': self.ajmscopy2,
            'xgft': self.xgft,
            'xgftcopy': self.xgftcopy,
            'sprq': self.sprq,
            'sprqcopy': self.sprqcopy,
            'sljg': self.sljg,
            'sljgcopy': self.sljgcopy,
            'sljgcopy2': self.sljgcopy2,
            'bycm': self.bycm,
            'bycmcopy': self.bycmcopy,
            'bycmcopy2': self.bycmcopy2,
            'sjy': self.sjy,
            'sjycopy2': self.sjycopy2,
            'bt': self.bt,
            'btcopy': self.btcopy,
            'fycj': self.fycj,
            'dy': self.dy,
            'nf': self.nf,
            'slcx': self.slcx,
            'ay': self.ay,
            'ft': self.ft,
            'tz': self.tz,
        }


class ElasticSearchClient(object):
    @staticmethod
    def get_es_servers():
        if 'ELASTICSEARCH_HOST' in environ and 'ELASTICSEARCH_PORT' in environ:
            host = environ['ELASTICSEARCH_HOST']
            port = environ['ELASTICSEARCH_PORT']
        else:
            host = 'localhost'
            port = 9200
            es_servers = [{'host': host, 'port': port}]
            es_client = Elasticsearch(hosts=es_servers, timeout=600)
        return es_client


class ElasticSearchUtils(object):
    def __init__(self, index='legal_index', doc_type='legalDocument'):
        self.index = index
        self.doc_type = doc_type
        self.es_client = ElasticSearchClient.get_es_servers()
        self.set_mappings_and_settings()

    def set_mappings_and_settings(self, analyzer='standard'):
        '''
        设置 mappings 和 settings
        '''
        settings = {
            'analysis': {
                'analyzer': {
                    'charsplit': {
                        'type': 'custom',
                        'tokenizer': 'ngram_tokenizer'
                    },
                    'standard': {
                        'type': 'standard'
                    }
                },
                'tokenizer': {
                    'ngram_tokenizer': {
                        'type': 'ngram',
                        'min_gram': 1,
                        'max_gram': 1,
                        'token_chars': ['letter', ' digit', 'punctuation']
                    }
                }
            }
        }

        mappings = {
            self.doc_type: {
                'properties': {
                    'id': {
                        'type': 'long'
                    },
                    'fy': {
                        'type': 'keyword'
                    },
                    'dsrxx': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'dsrxxcopy': {
                        'type': 'keyword'
                    },
                    'ah': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'ahcopy': {
                        'type': 'keyword'
                    },
                    'spry': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'sprycopy': {
                        'type': 'keyword'
                    },
                    'ysfycm': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'ysfycmcopy': {
                        'type': 'keyword'
                    },
                    'ysfycmcopy2': {
                        'type': 'keyword'
                    },
                    'ysqqqk': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'ysqqqkcopy': {
                        'type': 'keyword'
                    },
                    'ysqqqkcopy2': {
                        'type': 'keyword'
                    },
                    'byrw': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'byrwcopy': {
                        'type': 'keyword'
                    },
                    'byrwcopy2': {
                        'type': 'keyword'
                    },
                    'spjg': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'spjgcopy': {
                        'type': 'keyword'
                    },
                    'spjgcopy2': {
                        'type': 'keyword'
                    },
                    'ysdbqk': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'ysdbqkcopy': {
                        'type': 'keyword'
                    },
                    'ysdbqkcopy2': {
                        'type': 'keyword'
                    },
                    'esqqqk': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'esqqqkcopy': {
                        'type': 'keyword'
                    },
                    'esqqqkcopy2': {
                        'type': 'keyword'
                    },
                    'ysfyrw': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'ysfyrwcopy': {
                        'type': 'keyword'
                    },
                    'ysfyrwcopy2': {
                        'type': 'keyword'
                    },
                    'wslx': {
                        'type': 'keyword'
                    },
                    'ajms': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'ajmscopy': {
                        'type': 'keyword'
                    },
                    'ajmscopy2': {
                        'type': 'keyword'
                    },
                    'xgft': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'xgftcopy': {
                        'type': 'keyword'
                    },
                    'sprq': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'sprqcopy': {
                        'type': 'keyword'
                    },
                    'sljg': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'sljgcopy': {
                        'type': 'keyword'
                    },
                    'sljgcopy2': {
                        'type': 'keyword'
                    },
                    'bycm': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'bycmcopy': {
                        'type': 'keyword'
                    },
                    'bycmcopy2': {
                        'type': 'keyword'
                    },
                    'sjy': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'sjycopy': {
                        'type': 'keyword'
                    },
                    'sjycopy2': {
                        'type': 'keyword'
                    },
                    'bt': {
                        'analyzer': analyzer,
                        'type': 'text'
                    },
                    'btcopy': {
                        'type': 'keyword'
                    },
                    'fycj': {
                        'type': 'keyword'
                    },
                    'dy': {
                        'type': 'keyword'
                    },
                    'nf': {
                        'type': 'keyword'
                    },
                    'slcx': {
                        'type': 'keyword'
                    },
                    'ay': {
                        'type': 'keyword'
                    },
                    'tz': {
                        'analyzer': 'whitespace',
                        'type': 'text'
                    },
                    'ft': {
                        'analyzer': 'whitespace',
                        'type': 'text'
                    }
                }
            }
        }
        body = {
            'settings': settings,
            'mappings': mappings,
        }
        if not self.es_client.indices.exists(index=self.index):
            self.es_client.indices.create(
                index=self.index, body=body, ignore=400)
            # self.es_client.indices.put_mapping(
            #     index=self.index, doc_type=self.doc_type, body=mapping)

    def add_data(self, legal_doc):
        '''
        单条插入
        '''
        _id = legal_doc._id
        self.es_client.index(
            index=self.index,
            doc_type=self.doc_type,
            body=legal_doc.to_dict(),
            id=_id)

    def add_data_bulk(self, legal_docs, bulk_num=10):
        '''
        批量插入
        '''
        load_data = []
        cnt = 0
        for legal_doc in legal_docs:
            cnt += 1
            action = {
                '_index': self.index,
                '_type': self.doc_type,
                '_id': legal_doc.id,
                '_source': legal_doc.to_dict()
            }
            load_data.append(action)
            # 批量处理
            if len(load_data) == bulk_num:
                print('--- 插入 %d 批数据' % (cnt / bulk_num))
                success, failed = bulk(
                    self.es_client,
                    load_data,
                    index=self.index,
                    raise_on_error=True,
                    request_timeout=300)
                del load_data[0:len(load_data)]
                print('--- *****************************')
                print('--- ********** success **********')
                print('--- ' + str(success))
                print('--- *****************************')
                print('--- ********** failed ***********')
                print('--- ' + str(failed))
                print('--- ' + '*****************************')

        if len(load_data) > 0:
            success, failed = bulk(
                self.es_client,
                load_data,
                index=self.index,
                raise_on_error=True,
                request_timeout=300)
            del load_data[0:len(load_data)]
            print('--- *****************************')
            print('--- ********** success **********')
            print('--- ' + str(success))
            print('--- *****************************')
            print('--- ********** failed ***********')
            print('--- ' + str(failed))
            print('--- ' + '*****************************')


def add_data_test():
    legal_doc = LegalDocument()
    legal_doc.id = 10086
    legal_doc.fy = '123'
    legal_doc.dsrxx = '123'
    legal_doc.dsrxxcopy = '123'
    legal_doc.ah = '123'
    legal_doc.ahcopy = '123'
    legal_doc.spry = '123'
    legal_doc.sprycopy = '123'
    legal_doc.ysfycm = '123'
    legal_doc.ysfycmcopy = '123'
    legal_doc.ysfycmcopy2 = '12'
    legal_doc.ysqqqk = '1'
    legal_doc.ysqqqkcopy = '1'
    legal_doc.ysqqqkcopy2 = '1'
    legal_doc.byrw = '1'
    legal_doc.byrwcopy = '1'
    legal_doc.byrwcopy2 = '1'
    legal_doc.spjg = '1'
    legal_doc.spjgcopy = '1'
    legal_doc.spjgcopy2 = '1'
    legal_doc.ysdbqk = '1'
    legal_doc.ysdbqkcopy = '1'
    legal_doc.ysdbqkcopy2 = '1'
    legal_doc.esqqqk = '1'
    legal_doc.esqqqkcopy = '1'
    legal_doc.esqqqkcopy2 = '1'
    legal_doc.ysfyrw = '1'
    legal_doc.ysfyrwcopy = '1'
    legal_doc.ysfyrwcopy2 = '1'
    legal_doc.wslx = '1'
    legal_doc.ajms = '1'
    legal_doc.ajmscopy = '1'
    legal_doc.ajmscopy2 = '1'
    legal_doc.xgft = '1'
    legal_doc.xgftcopy = '1'
    legal_doc.sprq = '1'
    legal_doc.sprqcopy = '1'
    legal_doc.sljg = '1'
    legal_doc.sljgcopy = '1'
    legal_doc.sljgcopy2 = '2'
    legal_doc.bycm = '2'
    legal_doc.bycmcopy = '2'
    legal_doc.bycmcopy2 = '2'
    legal_doc.sjy = '2'
    legal_doc.sjycopy2 = '2'
    legal_doc.bt = '2'
    legal_doc.btcopy = '2'
    legal_doc.fycj = '2'
    legal_doc.dy = '2'
    legal_doc.nf = '2'
    legal_doc.slcx = '2'
    legal_doc.ay = '2'
    legal_doc.ft = '22'
    legal_doc.tz = '22'

    es_utils = ElasticSearchUtils()
    es_utils.add_data(legal_doc)


def add_data_bulk_test():
    legal_docs = []
    for i in range(0, 100):
        legal_doc = LegalDocument()
        legal_doc.id = i
        legal_doc.fy = '123'
        legal_doc.dsrxx = '123'
        legal_doc.dsrxxcopy = '123'
        legal_doc.ah = '123'
        legal_doc.ahcopy = '123'
        legal_doc.spry = '123'
        legal_doc.sprycopy = '123'
        legal_doc.ysfycm = '123'
        legal_doc.ysfycmcopy = '123'
        legal_doc.ysfycmcopy2 = '12'
        legal_doc.ysqqqk = '1'
        legal_doc.ysqqqkcopy = '1'
        legal_doc.ysqqqkcopy2 = '1'
        legal_doc.byrw = '1'
        legal_doc.byrwcopy = '1'
        legal_doc.byrwcopy2 = '1'
        legal_doc.spjg = '1'
        legal_doc.spjgcopy = '1'
        legal_doc.spjgcopy2 = '1'
        legal_doc.ysdbqk = '1'
        legal_doc.ysdbqkcopy = '1'
        legal_doc.ysdbqkcopy2 = '1'
        legal_doc.esqqqk = '1'
        legal_doc.esqqqkcopy = '1'
        legal_doc.esqqqkcopy2 = '1'
        legal_doc.ysfyrw = '1'
        legal_doc.ysfyrwcopy = '1'
        legal_doc.ysfyrwcopy2 = '1'
        legal_doc.wslx = '1'
        legal_doc.ajms = '1'
        legal_doc.ajmscopy = '1'
        legal_doc.ajmscopy2 = '1'
        legal_doc.xgft = '1'
        legal_doc.xgftcopy = '1'
        legal_doc.sprq = '1'
        legal_doc.sprqcopy = '1'
        legal_doc.sljg = '1'
        legal_doc.sljgcopy = '1'
        legal_doc.sljgcopy2 = '2'
        legal_doc.bycm = '2'
        legal_doc.bycmcopy = '2'
        legal_doc.bycmcopy2 = '2'
        legal_doc.sjy = '2'
        legal_doc.sjycopy2 = '2'
        legal_doc.bt = '2'
        legal_doc.btcopy = '2'
        legal_doc.fycj = '2'
        legal_doc.dy = '2'
        legal_doc.nf = '2'
        legal_doc.slcx = '2'
        legal_doc.ay = '2'
        legal_doc.ft = '22'
        legal_doc.tz = '22'

        legal_docs.append(legal_doc)

    es_utils = ElasticSearchUtils()
    es_utils.add_data_bulk(legal_docs)


if __name__ == '__main__':
    add_data_test()
    add_data_bulk_test()
