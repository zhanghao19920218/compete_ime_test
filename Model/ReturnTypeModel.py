# coding: utf-8

from Parameter import ErrorInfoType
from typing import List


class ReturnTypeModel:
    """
    返回候选词属性
    """

    def __init__(self,
                 origin_json: str,
                 cloud_list: List[str],
                 candidate_list: List[str],
                 target_pos: int,
                 last_word: str,
                 is_name_pattern: bool,
                 candidate_length: int):
        """
        初始化
        :param origin_json: 原始json文件
        :param cloud_list: 云端解码结果
        :param candidate_list: 候选词结果
        :param candidate_length: 候选词长度
        :param target_pos: 获取词汇位置
        :param last_word: 最后上屏的词
        :param is_name_pattern: 是不是人名模式
        """
        self.origin_json = origin_json
        self.cloud_list = cloud_list
        self.candidate_list = candidate_list
        self.candidate_length = candidate_length
        self.target_pos = target_pos
        self.last_word = last_word
        self.is_name_pattern = is_name_pattern


class DecodeReturnModel:
    """
    返回候选词属性
    """

    def __init__(self,
                 associate_list: List[str],
                 origin_json_str: str,
                 cloud_list: List[str],
                 candidate_list: List[str],
                 target_pos: int,
                 net_work_status: bool,
                 time_stamp: str,
                 last_word: str,
                 is_name_pattern: bool,
                 error_type: ErrorInfoType):
        """
        初始化
        :param associate_list: 联想结果
        :param cloud_list: 云端结果
        :param candidate_list: 候选词结果
        :param target_pos: 当前的位置
        :param origin_json_str: 原始的json内容
        :param net_work_status: 网络状态是否正常
        :param time_stamp: 时间戳
        :param is_name_pattern: 是否触发人名模式
        :param last_word: 最后屏显的词
        """
        self.associate_list = associate_list
        self.cloud_list = cloud_list
        self.origin_json_str = origin_json_str
        self.candidate_list = candidate_list
        self.error_type = error_type
        self.target_pos = target_pos
        self.net_work_status = net_work_status
        self.time_stamp = time_stamp
        self.last_word = last_word
        self.is_name_pattern = is_name_pattern
