# coding: utf-8
# 匹配解码的对象

class MatchScreenInputModel:
    grape_word: str  # 需要抓取的词

    above_word: str  # 需要上屏的词

    def __init__(self,
                 grape_word: str,
                 above_word: str):
        """
        初始化选词的Object
        :param grape_word: 需要抓取的拼音
        :param above_word:  上屏的词
        """
        self.grape_word = grape_word
        self.above_word = above_word
