# coding=utf-8
# @author: haozhang45
# @date: 2022/3/21
# @description: 引擎测试集对应的方法名称
from enum import Enum


class EngineMethod(Enum):
    """
    引擎方法的枚举
    """
    INIT_ENGINE = "#INIT_ENGINE"  # 初始化引擎
    SWAP_METHOD = "#SWAP_METHOD"  # 切换方法
    INPUT_KEYS_RANDOM = "#INPUT_KEYS_RANDOM"  # 随机输入
    GET_ASSOCIATE = "#GET_ASSOCIATE"  # 获取联想结果
    INPUT_KEYS = "#INPUT_KEYS"  # 按键输入
    GET_WORDS = "#GET_WORDS"  # 获取解码结果
    SELECT_WORD = "#SELECT_WORDS"  # 选词结果
    RESET = "#RESET"  # 重置
    RELEASE_ENGINE = "#RELEASE_ENGINE"  # 引擎释放
    DELETE = "#DELETE"  # 回删一位


class EngineMethodAction(object):
    """
    Get engine method pair name
    """

    @property
    def method_name(self) -> EngineMethod:
        """
        get engine action type
        :return:
        """
        return self._method_name

    @property
    def method_action(self) -> str:
        """
        get the str detail of engine method
        :return:
        """
        if self._method_name in [EngineMethod.RELEASE_ENGINE, EngineMethod.RESET]:
            # if the method in these engine actions, will return empty str
            return ""
        return self._method_action

    def __init__(self,
                 method_name: EngineMethod,
                 method_action: str):
        self._method_name = method_name
        self._method_action = method_action


class EngineKeyboardType(Enum):
    """
    引擎按键方法
    """
    NINE_KEY_BOARD = "9key"
    TWENTY_SIX_BOARD = "26key"


class EngineInputType(Enum):
    """
    引擎输入类型
    """
    PINYIN = "pinyin"
    PINYIN_EN = "pinyin+english"
    EN = "english"


class FuzzyType(Enum):
    """
    纠错模式
    """
    FUZZY_KEY = "fuzzykey"
    NO_FUZZY_KEY = "no fuzzy key"
