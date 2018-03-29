from django.db import models


class LegalDocument():
    # 构造函数,id,法院，当事人信息，案号，审判人员，一审法院查明
    def __init__(self):
        self.id = 0
        self.similarity=0
        self.fy = ""
        self.dsrxx = ""
        self.dsrxxcopy = ""
        self.ah = ""
        self.ahcopy = ""
        self.spry = ""
        self.sprycopy = ""
        self.ysfycm = ""
        self.ysfycmcopy = ""
        self.ysfycmcopy2 = ""
        self.ysqqqk = ""
        self.ysqqqkcopy = ""
        self.ysqqqkcopy2 = ""
        self.byrw = ""
        self.byrwcopy = ""
        self.byrwcopy2 = ""
        self.spjg = ""
        self.spjgcopy = ""
        self.spjgcopy2 = ""
        self.ysdbqk = ""
        self.ysdbqkcopy = ""
        self.ysdbqkcopy2 = ""
        self.esqqqk = ""
        self.esqqqkcopy = ""
        self.esqqqkcopy2 = ""
        self.ysfyrw = ""
        self.ysfyrwcopy = ""
        self.ysfyrwcopy2 = ""
        self.wslx = ""
        self.ajms = ""
        self.ajmscopy = ""
        self.ajmscopy2 = ""
        self.xgft = ""
        self.xgftcopy = ""
        self.sprq = ""
        self.sprqcopy = ""
        self.sljg = ""
        self.sljgcopy = ""
        self.sljgcopy2 = ""
        self.bycm = ""
        self.bycmcopy = ""
        self.bycmcopy2 = ""
        self.sjy = ""
        self.sjycopy2 = ""
        self.bt = ""
        self.btcopy = ""
        self.fycj = ""
        self.dy = ""
        self.nf = ""
        self.slcx = ""
        self.ay = ""
        self.ft = ""
        self.tz = ""

    def to_dict(self):
        '''
        将 LegalDocument 内的所有内容用字典打包
        '''
        return {
            'id': self.id,
            'similirity':self.similarity,
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

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id


class SearchStruct():
    def __init__(self):
        self.allFieldKeyWord = []
        self.oneFieldKeyWord = {}
        self.allFieldNotKeyWord = []
        self.oneFieldNotKeyWord = {}
        self.FieldKeyWord = []
        self.OrderFieldKey = []

    def print(self):
        return {
            '全域搜索': self.allFieldKeyWord,
            '单领域搜索': self.oneFieldKeyWord,
            '全域否定搜索': self.allFieldNotKeyWord,
            '单域否定搜索': self.oneFieldNotKeyWord,
            '同域搜索': self.FieldKeyWord,
            '顺序搜索': self.OrderFieldKey

        }

    # 数据格式为列表
    @property
    def allFieldKeyWord(self):
        return self._allFieldKeyWord

    @allFieldKeyWord.setter
    def allFieldKeyWord(self, allFieldKeyWord):
        self._allFieldKeyWord = allFieldKeyWord

    # 数据格式为字典
    @property
    def oneFieldKeyWord(self):
        return self._oneFieldKeyWord

    @oneFieldKeyWord.setter
    def oneFieldKeyWord(self, oneFieldKeyWord):
        self._oneFieldKeyWord = oneFieldKeyWord

    @property
    def allFieldKeyWord(self):
        return self._allFieldKeyWord

    @allFieldKeyWord.setter
    def allFieldKeyWord(self, allFieldKeyWord):
        self._allFieldKeyWord = allFieldKeyWord

    @property
    def allFieldKeyWord(self):
        return self._allFieldKeyWord

    @allFieldKeyWord.setter
    def allFieldKeyWord(self, allFieldKeyWord):
        self._allFieldKeyWord = allFieldKeyWord

    @property
    def allFieldKeyWord(self):
        return self._allFieldKeyWord

    @allFieldKeyWord.setter
    def allFieldKeyWord(self, allFieldKeyWord):
        self._allFieldKeyWord = allFieldKeyWord

    def clear(self):
        self.allFieldKeyWord = []
        self.oneFieldKeyWord = {}
        self.allFieldNotKeyWord = []
        self.oneFieldNotKeyWord = {}
        self.FieldKeyWord = []
        self.OrderFieldKey = []
