import urllib
import urllib.request


class Parser(object):
    '''
    读取文件，并对其进行分词
    （运用 lpt 平台）
    '''

    def __init__(self,
                 path,
                 api_key='M2R6x2Q6NVnVgjLbhP1pyT0QyLxXTVwZLrrmNzEY',
                 sign='##',
                 ignored_list=['案由', '引用法条', '特征']):
        '''
        sign: 文件中分隔符
        target_list: 需要分离的字段
        '''
        self._path = path
        self._api_key = api_key
        self._sign = sign
        self._ignored_list = set(ignored_list)

    def analyze(self):
        self._pack = {}
        '''
        读取文件，并对文件内的字符串进行分词
        （只分在 target_list 内的字段）
        '''
        f = open(self._path, 'r')
        for _ in f.readlines():
            key, content = _.split(self._sign)
            if key in self._ignored_list:
                self.pack[key] = content
            else:
                self.pack[key] = self._lpt_helper(content)

    def _lpt_helper(self, content):
        url_base = 'https://api.ltp-cloud.com/analysis/?'
        args = {
            'api_key': self._api_key,
            'text': content,
            'format': 'conll',
            'pattern': 'dp',
        }
        args = urllib.parse.urlencode(args).encode(encoding='utf-8')
        response = urllib.request.urlopen(url_base, args)
        content = str(response.read(),
                      'utf-8').replace('\t', ' ').strip().split('\n')
        return content

    @property
    def pack(self):
        '''
        返回 pack
        '''
        return self._pack

    @pack.setter
    def pack(self, value):
        self._pack = value

    @pack.deleter
    def pack(self):
        del self._pack


if __name__ == '__main__':
    path = '/home/cowlog/Dropbox/Project/刑事/提取/00001.txt'
    p = Parser(path=path)  # api_key='v1L7l1D825BCVgHyLC5nyzafeHYVtDmD9eUbsTKR'
    p.analyze()
    res = p.pack
    print(res)
