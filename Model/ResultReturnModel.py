# coding: utf-8
import json


class CandidateModel:
    """获取候选词的Model"""

    def __init__(self,
                 cloud: str,
                 force_cloud: str,
                 local_sign: list,
                 candidates_list: str,
                 last_word: str,
                 start: int,
                 target: int,
                 end: int):
        self.cloud = cloud
        self.force_cloud = force_cloud
        self.local_sign = local_sign
        self.last_word = last_word
        if type(candidates_list) == list:
            self.candidates_list = candidates_list
        elif isinstance(candidates_list, str):
            self.candidates_list = candidates_list.split(',')
        else:
            self.candidates_list = []
        self.start = start
        self.end = end
        self.target = target

    @staticmethod
    def dict_to_object(d):
        """从字典转化成Model"""
        return CandidateModel(
            cloud=d.get('cloud') if 'cloud' in d else None,
            force_cloud=d.get('forcecloud') if 'forcecloud' in d else None,
            local_sign=d.get('localsign'),
            candidates_list=d.get('list') if 'list' in d else [],
            start=d.get('start'),
            end=d.get('end'),
            target=d.get('target'),
            last_word=d.get('last_position') if 'last_position' in d else ''
        )

    def to_json(self):
        """model转化成json"""
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False,
                          sort_keys=False)  # 按照顺序解析

    def to_dict(self):
        d: dict = {}
        for key, value in self.__dict__.items():
            if type(value) is CandidateModel:
                value = value.to_dict()
            d[key] = value
        return d


class ComposeDetailInfoModel:
    """
    详细解码的结果
    """

    def __init__(self,
                 composing: str,
                 status: str,
                 mode: str,
                 layout: str,
                 is_name_pattern: str,
                 candidates: dict,
                 last_word: str):
        self.composing = composing
        self.status = status
        self.mode = mode
        self.layout = layout
        self.is_name_pattern = int(is_name_pattern) == 1
        self.candidates = CandidateModel.dict_to_object(candidates)
        self.last_word = last_word

    @staticmethod
    def dict_to_object(d):
        """从字典转化成Model"""
        return ComposeDetailInfoModel(
            composing=d.get('composing'),
            status=d.get('status'),
            mode=d.get('mode'),
            layout=d.get('layout'),
            is_name_pattern=d.get('is_name_pattern') if 'is_name_pattern' in d.keys() else '0',
            candidates=d.get('candidates'),
            last_word=d.get('last_word') if 'last_word' in d.keys() else ''
        )

    def to_json(self):
        """model转化成json"""
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False,
                          sort_keys=False)  # 按照顺序解析

    def to_dict(self):
        d: dict = {}
        for key, value in self.__dict__.items():
            if type(value) is ComposeDetailInfoModel:
                value = value.to_dict()
            d[key] = value
        return d


class ResultInfoModel:
    """详细信息的Model"""

    def __init__(self,
                 success: bool,
                 result: dict,
                 failed_reason: str):
        self.success = success
        self.failed_reason = failed_reason
        self.result = ComposeDetailInfoModel.dict_to_object(result)  # 转化成Model

    @staticmethod
    def dict_to_object(d):
        """从字典转化成Model"""
        return ResultInfoModel(
            success=d.get('success'),
            result=d.get('result') if 'result' in d.keys() else None,
            failed_reason=d.get('failed_reason')
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


class DetailReturnModel:
    """返回详细的结果"""

    def __init__(self,
                 result: str):
        json_dict = json.loads(result)
        self.result = ResultInfoModel.dict_to_object(json_dict)
        self.origin_json = result

    @staticmethod
    def dict_to_object(d):
        """从字典转化成Model"""
        return DetailReturnModel(
            result=d.get('result')
        )

    def to_json(self):
        """model转化成json"""
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False,
                          sort_keys=False)  # 按照顺序解析

    def to_dict(self):
        d: dict = {}
        for key, value in self.__dict__.items():
            if type(value) is DetailReturnModel:
                value = value.to_dict()
            d[key] = value
        return d


class ResultReturnModel:
    """返回的数据的Model"""

    def __init__(self,
                 success: bool,
                 result: dict,
                 failed_reason: str):
        self.success = success
        self.failed_reason = failed_reason
        self.result: DetailReturnModel = DetailReturnModel.dict_to_object(result)  # 转化成Model

    @staticmethod
    def dict_to_object(d):
        """从字典转化成Model"""
        return ResultReturnModel(
            success=d.get('success'),
            result=d.get('result') if 'result' in d.keys() else None,
            failed_reason=d.get('failed_reason')
        )

    def to_json(self):
        """model转化成json"""
        return json.dumps(self, default=lambda obj: obj.__dict__, ensure_ascii=False,
                          sort_keys=False)  # 按照顺序解析

    def to_dict(self):
        d: dict = {}
        for key, value in self.__dict__.items():
            if type(value) is ResultReturnModel:
                value = value.to_dict()
            d[key] = value
        return d
