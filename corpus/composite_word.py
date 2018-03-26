from operator import itemgetter


class CompositeRule(object):
    def __init__(self, before_word_count, after_word_count, before_word_class,
                 after_word_class, relationship):
        '''
        before_word_count: 前一个词字数
        after_word_count: 后一个词字数
        before_word_class: 前一个词词性
        after_word_class: 后一个词词性
        relationship: 两个词关系
        '''
        self._before_word_count = before_word_count
        self._after_word_count = after_word_count
        self._before_word_class = before_word_class
        self._after_word_class = after_word_class
        self._relationship = relationship

    def wrapper_to_dict(self):
        return {
            'before_word_count': self.before_word_count,
            'after_word_count': self.after_word_count,
            'before_word_class': self.before_word_class,
            'after_word_class': self.after_word_class,
            'relationship': self.relationship,
        }

    def compare(self, before_word, after_word, before_word_class,
                after_word_class, relationship):
        '''
        比较函数

        before_word: 前一个词
        after_word: 后一个词
        before_word_class: 前一个词词性
        after_word_class: 后一个词词性
        relationship: 两个词关系
        '''
        return len(before_word) == self.before_word_count and \
            len(after_word) == self.after_word_count and \
            before_word_class == self.before_word_class and \
            after_word_class == self.after_word_class and \
            relationship == self.relationship

    @property
    def before_word_count(self):
        return self._before_word_count

    @before_word_count.setter
    def before_word_count(self, value):
        self._before_word_count = value

    @before_word_count.deleter
    def before_word_count(self):
        del self._before_word_count

    @property
    def after_word_count(self):
        return self._after_word_count

    @after_word_count.setter
    def after_word_count(self, value):
        self._after_word_count = value

    @after_word_count.deleter
    def after_word_count(self):
        del self._after_word_count

    @property
    def before_word_class(self):
        return self._before_word_class

    @before_word_class.setter
    def before_word_class(self, value):
        self._before_word_class = value

    @before_word_class.deleter
    def before_word_class(self):
        del self._before_word_class

    @property
    def after_word_class(self):
        return self._after_word_class

    @after_word_class.setter
    def after_word_class(self, value):
        self._after_word_class = value

    @after_word_class.deleter
    def after_word_class(self):
        del self._after_word_class

    @property
    def relationship(self):
        return self._relationship

    @relationship.setter
    def relationship(self, value):
        self._relationship = value

    @relationship.deleter
    def relationship(self):
        del self._relationship


class CompositeWord(object):
    def __init__(self,
                 source,
                 source_sign=' ',
                 rules=[
                     CompositeRule(2, 2, 'n', 'nz', 'ATT'),
                     CompositeRule(1, 2, 'n', 'nz', 'ATT'),
                     CompositeRule(2, 2, 'n', 'n', 'ATT'),
                     CompositeRule(2, 2, 'nz', 'nz', 'ATT')
                 ],
                 position=[1, 4, 7],
                 ignored_list='。？！，、；：“”‘’（）【】……－-～·《》'):
        '''
        source: 已经经 lpt 处理的 conll 文本列表
        source_sign: 切割符号
        rules: 合成规则
        position: 需要取 conll 文本的列位置

        _comsposite_word: 按照规则已经找到的合成词
        '''
        self._source = source
        self._source_sign = source_sign
        self._rules = rules
        self._position = position
        self._ignored_list = ignored_list
        self._composite_word = []

        self.find_composite_words()
        self.make_new_list()

    def find_composite_words(self):
        '''
        根据规则判断合成词，生成词列表
        '''
        length = len(self.source)
        word = ''
        word_class = ''
        for i in range(1, length):
            prev_word, prev_word_class, prev_word_relationship = itemgetter(
                *self.position)(self.source[i - 1].split(self.source_sign))
            curr_word, curr_word_class, curr_word_relationship = itemgetter(
                *self.position)(self.source[i].split(self.source_sign))
            for rule in self.rules:
                if rule.compare(prev_word, curr_word, prev_word_class,
                                curr_word_class, curr_word_relationship):
                    if not word:
                        word = prev_word
                    word += curr_word
                    word_class = curr_word_class
                else:
                    if word:
                        self._composite_word.append((word, word_class))
                    word = ''
                    word_class = ''

    def make_new_list(self, sign=None):
        '''
        生成新的词表 (词)
        '''
        if sign is None:
            sign = self.source_sign

        self._new_list = []

        # 处理非复合词
        for _ in self.source:
            word = _.split(self.source_sign)[self.position[0]]
            if word in self.ignored_list:
                continue
            # 没有复合词
            if not self.composite_word:
                self._new_list.append(word)

            else:
                for composite_word, __ in self.composite_word:
                    if word not in composite_word:
                        self._new_list.append(word)

        # 处理复合词
        for word, _ in self.composite_word:
            self._new_list.append(word)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @source.deleter
    def source(self):
        del self._source

    @property
    def source_sign(self):
        return self._source_sign

    @source_sign.setter
    def source_sign(self, value):
        self._source_sign = value

    @source_sign.deleter
    def source_sign(self):
        del self._source_sign

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value

    @rules.deleter
    def rules(self):
        del self._rules

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @position.deleter
    def position(self):
        del self._position

    @property
    def ignored_list(self):
        return self._ignored_list

    @ignored_list.setter
    def ignored_list(self, value):
        self._ignored_list = value

    @ignored_list.deleter
    def ignored_list(self):
        del self._ignored_list

    @property
    def composite_word(self):
        return self._composite_word

    @composite_word.setter
    def composite_word(self, value):
        self._composite_word = value

    @composite_word.deleter
    def composite_word(self):
        del self._composite_word

    @property
    def new_list(self):
        return self._new_list

    @new_list.setter
    def new_list(self, value):
        self._new_list = value

    @new_list.deleter
    def new_list(self):
        del self._new_list


if __name__ == '__main__':
    f = open('/home/cowlog/Project/刑事/分词.txt', 'r')
    for line in f.readlines():
        _, content = line.split('##')
        for s in content.split('$$$'):
            source = s.split('#')[:-1]
            print(CompositeWord(source).new_list)
