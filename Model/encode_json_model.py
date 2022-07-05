# coding=utf-8
# @author: haozhang45
# @date: 2022/1/7
# @description: 将结果转为一个json数据
import json
from typing import List
from Parameter import ErrorInfoType


class EncodeJsonModel(object):
    # 输入
    input_keys: str = ""

    # 期望值
    expect_word: str = ""

    # 候选词
    candidates: List[str] = []

    # 期望联想
    expect_associate: str = ""

    # 错误信息
    error_type: ErrorInfoType = ErrorInfoType.Success

    # 选词位置
    input_num: int = 0

    # 日期
    time_stamp: str = ""

    # 是否有网络
    is_net_connect: bool = False

    # 是否需要计数
    is_calculate: bool = False

    # 联想候选
    associate_candi: List[str] = []

    # 云端结果
    cloud_candi: List[str] = []

    # 是否需要时间戳
    is_need_time_stamp: bool = False

    # 最后一位的显屏词
    last_word: str = ""

    # 是否触发人名模式
    is_name_pattern: bool = False

    def model_to_json(self) -> str:
        """
        将对象转为一个json数据
        :return:
        """
        origin_dict: dict = {'input': self.input_keys, 'expect_word': self.expect_word, 'cloud_word': self.cloud_candi, 'last_word': self.last_word}
        if self.error_type != ErrorInfoType.Success:
            origin_dict['error'] = '解码错误' if self.error_type == ErrorInfoType.DecodeError else '超出选词步数'
        else:
            origin_dict['candidates'] = self.candidates
            origin_dict['expect_ass'] = self.expect_associate
            origin_dict['ass_candi'] = self.associate_candi
        if self.is_calculate:
            origin_dict['input_num'] = self.input_num
        if self.is_net_connect:
            origin_dict['network'] = "connect error"
        if self.is_need_time_stamp:
            origin_dict['time_stamp'] = self.time_stamp
        origin_dict['is_name_pattern'] = '1' if self.is_name_pattern else '0'
        return json.dumps(origin_dict, ensure_ascii=False)



