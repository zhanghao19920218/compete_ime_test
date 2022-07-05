# coding: utf-8

class InputItemObj:
    grape_word: str  # 需要抓取的词

    above_word: str  # 需要上屏的词

    associate_word: str  # 联想词

    is_need_commit: bool

    def __init__(self, grape_word: str, above_word: str, associate_word: str, is_need_commit: bool):
        """
        初始化选词的Object
        :param grape_word: 需要抓取的拼音
        :param above_word:  上屏的词
        :param is_need_commit: 是否需要上屏
        :param associate_word: 联想词汇
        """
        self.grape_word = grape_word
        self.above_word = above_word
        self.associate_word = associate_word
        self.is_need_commit = is_need_commit


class DoubleCommitModel:
    grape_word: str  # 需要抓取的词

    above_word: str  # 需要上屏的词

    def __init__(self, grape_word: str, above_word: str):
        """
        初始化选词的Object
        :param grape_word: 需要抓取的拼音
        :param above_word:  上屏的词
        """
        self.grape_word = grape_word
        self.above_word = above_word
