# coding=utf-8
# @author: haozhang45
# @date: 2022/3/21
# @description:  引擎测试集解码的接口类
from abc import ABCMeta, abstractmethod, abstractproperty


class EngineInterface(metaclass=ABCMeta):

    @abstractmethod
    def engine_method_dict(self) -> dict:
        """
        引擎字典
        :return:
        """
        pass

    @abstractmethod
    def init_engine(self):
        """
        初始化引擎
        :return:
        """
        pass

    @abstractmethod
    def swap_method(self):
        """
        切换方法
        :return:
        """
        pass

    @abstractmethod
    def input_keys(self):
        """
        输入按键
        :return:
        """
        pass

    @abstractmethod
    def get_words(self):
        """
        获取解码结果
        :return:
        """
        pass

    @abstractmethod
    def select_word(self):
        """
        选词
        :return:
        """

    @abstractmethod
    def reset_engine(self):
        """
        重置输入
        :return:
        """
        pass

    @abstractmethod
    def release_engine(self):
        """
        释放引擎
        :return:
        """
        pass

    @abstractmethod
    def get_associate(self):
        """
        联想结果获取
        :return:
        """

