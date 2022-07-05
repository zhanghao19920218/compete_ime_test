# coding=utf-8
# @author: haozhang45
# @date: 2022/3/21
# @description:

from Parameter import InputCom, KeyboardType, TestType


class EngineConfigModel(object):
    """
    引擎测试集测试的配置model
    """
    # 键盘厂商
    _ime_type: InputCom
    # 按键类型
    _keyboard_type: KeyboardType
    # 测试的类型
    _test_type: TestType

    @property
    def ime_type(self):
        """
        获取按键品牌
        :return:
        """
        return self._ime_type

    @property
    def keyboard_type(self):
        """
        按键类型
        :return:
        """
        return self._keyboard_type

    @property
    def test_type(self):
        """
        测试类型
        :return:
        """
        return self._test_type

    def __init__(self,
                 ime_type: InputCom,
                 keyboard_type: KeyboardType,
                 test_type: TestType):
        """
        初始化函数
        :param ime_type:
        :param keyboard_type:
        :param test_type:
        """
        self._test_type = test_type
        self._keyboard_type = keyboard_type
        self._ime_type = ime_type

