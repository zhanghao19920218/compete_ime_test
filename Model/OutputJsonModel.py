# coding: utf-8
import json


class ResultInfoModel:
    """解码result字段"""

    def __init__(self,
                 candidates: str,
                 cloud: str,
                 last_word: str,
                 target: int):
        filter_str: str = candidates.replace(" ", "").strip("[]")
        if len(filter_str) == 0:  # 如果解码为空字符就是空数组
            self.candidates = []
        else:
            self.candidates = filter_str.split(',')
        self.cloud = cloud
        self.target = target
        self.last_word = last_word

    @staticmethod
    def dict_to_object(d: dict):
        """从字典转化成Model"""
        return ResultInfoModel(
            candidates=d.get('candidates') if 'candidates' in d.keys() else "[]",
            cloud=d.get('cloud') if 'cloud' in d.keys() else None,
            target=d.get('target') if 'target' in d.keys() else 0,
            last_word=d.get('last_position')
        )

    def to_json(self):
        """model转化成json"""
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False,
                          sort_keys=False)  # 按照顺序解析

    def to_dict(self):
        d: dict = {}
        for key, value in self.__dict__.items():
            if type(value) is ResultInfoModel:
                value = value.to_dict()
            d[key] = value
        return d


class OutputJsonModel:
    """解码socket传输数据"""

    def __init__(self,
                 success: bool,
                 result: dict,
                 failed_reason: str):
        self.success = success
        self.failed_reason = failed_reason
        self.result = ResultInfoModel.dict_to_object(result)  # 转化成Model

    @staticmethod
    def dict_to_object(d):
        """从字典转化成Model"""
        if d:
            return OutputJsonModel(
                success=d.get('success'),
                result=d.get('result') if 'result' in d.keys() else None,
                failed_reason=d.get('failed_reason')
            )
        else:
            return OutputJsonModel(
                success=False,
                result={},
                failed_reason=""
            )

    def to_json(self):
        """model转化成json"""
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False,
                          sort_keys=False)  # 按照顺序解析

    def to_dict(self):
        d: dict = {}
        for key, value in self.__dict__.items():
            if type(value) is OutputJsonModel:
                value = value.to_dict()
            d[key] = value
        return d
