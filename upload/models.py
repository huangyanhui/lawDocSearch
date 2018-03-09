from django.db import models

# Create your models here.
class LegalDocument():
    #构造函数,id,法院，当事人信息，案号，审判人员，一审法院查明
    def __init__(self):
        self.id=0
        self.fy=""
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
        self.spjgcopy2=""
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


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        self._id=id
