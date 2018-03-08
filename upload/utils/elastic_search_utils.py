# from lawDoc.models import LegalDocument

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
