# coding: utf-8
# 返回上下文写入文件的Model
import json

from Parameter import ErrorInfoType


class WriteConnectionModel:
    candidate_list: [str] = []

    cloud_list: [str] = []

    above_word: str = ""

    origin_json_str: str = ""

    grape_word: str = ""

    last_word: str = ""

    previous_word: str = ""

    error_type: ErrorInfoType = ErrorInfoType.Success

    def __init__(self,
                 candidate_list: [str],
                 cloud_list: [str],
                 above_word: str,
                 grape_word: str,
                 origin_json_str: str,
                 last_word: str,
                 previous_word: str,
                 error_type: ErrorInfoType):
        """
        初始化
        :param candidate_list:  候选词
        :param cloud_list:  云端解码
        :param above_word:  上屏测绘
        :param grape_word:  拼音
        :param origin_json_str:  初始化
        :param error_type: 错误类型
        :param last_word: 最后屏显词
        :param previous_word: 前缀词
        """
        self.candidate_list = candidate_list
        self.cloud_list = cloud_list
        self.above_word = above_word
        self.grape_word = grape_word
        self.origin_json_str = origin_json_str
        self.error_type = error_type
        self.last_word = last_word

    def model_to_json(self) -> str:
        """
        将对象转为一个json数据
        :return:
        """
        origin_dict: dict = {'input': self.grape_word, 'expect_word': self.above_word, 'cloud_word': self.cloud_list,
                             'last_word': self.last_word}
        if self.error_type != ErrorInfoType.Success:
            origin_dict['error'] = '解码错误' if self.error_type == ErrorInfoType.DecodeError else '超出选词步数'
        else:
            origin_dict['candidates'] = self.candidate_list
        return json.dumps(origin_dict, ensure_ascii=False)
