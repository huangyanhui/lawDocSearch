from django.db import models

# Create your models here.
class LegalDocument():
    #构造函数,id,法院，当事人信息，案号，审判人员，一审法院查明
    def __init__(self,id,fy,dsrxx,ah,spry):
        self.id=None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        self._id=id

class SearchStruct():
    def __init__(self):
        self.allFieldKeyWord=[]
        self.oneFieldKeyWord={}
        self.allFieldNotKeyWord=[]
        self.oneFieldNotKeyWord={}
        self.FieldKeyWord=[]
        self.OrderFieldKey=[]

    #数据格式为列表
    @property
    def allFieldKeyWord(self):
        return self._allFieldKeyWord

    @allFieldKeyWord.setter
    def allFieldKeyWord(self,allFieldKeyWord):
        self._allFieldKeyWord=allFieldKeyWord

    #数据格式为字典
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



