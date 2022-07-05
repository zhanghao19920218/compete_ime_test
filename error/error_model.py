# coding: utf-8
from enum import Enum


class AppiumErrorType(Enum):
    """
    The error create from the appium runtime
    """
    NO_DEVICE_CONNECT = "No Device Connection"

    DRIVER_ERROR = "Appium driver Error"

    OTHER_ERROR = "Other Errors"


class Error(Exception):
    """
    此模块的基本异常类
    """
    pass


class EmulatorError(Error):
    """
    模拟器异常

    Attributes:
         message -- 错误描述
    """
    message: str = ""

    def __init__(self,
                 message):
        """
        初始化错误信息
        :param message:
        """
        self.message = message


class AppiumError(Error):
    """
    Appium错误
    
    Attributes:
         message -- 错误信息
    """
    message: str = ""

    _error_type: AppiumErrorType

    @property
    def get_error_type(self) -> AppiumErrorType:
        """
        Return error type
        :return:
        """
        return self._error_type

    def __init__(self,
                 error_type: AppiumErrorType = AppiumErrorType.OTHER_ERROR,
                 message: str = ""):
        self._error_type = error_type
        self.message = message

    def to_string(self) -> str:
        """
        Convert to print message info
        If not contains in Appium Error enum, it will print message info
        :return:
        """
        if self._error_type == AppiumErrorType.NO_DEVICE_CONNECT:
            return AppiumErrorType.NO_DEVICE_CONNECT.value
        else:
            return self.message


class InputError(Error):
    """
       键盘输入的值异常

       Attributes:
            message -- 错误描述
       """
    message: str = ""

    value: int = 0

    def __init__(self,
                 message,
                 value):
        """
        初始化错误信息
        :param message:
        :param value: 错误值
        """
        self.message = message
        self.value = value


class EngineErrorEnum(Enum):
    """
    enumerate the engine error case
    """
    SWAP_METHOD_ERROR = 1  # swap method cause error


class EngineTCError(Error):
    """
    engine test case raise error
    """
    _engine_error_type: EngineErrorEnum

    _error_message: str

    @property
    def engine_error_type(self) -> EngineErrorEnum:
        """
        get the detail Engine Test Case Error Info
        :return:
        """
        return self._engine_error_type

    @property
    def error_message(self) -> str:
        """
        detail error information
        :return:
        """
        return self._error_message

    def __init__(self,
                 error_type: EngineErrorEnum,
                 message: str):
        self._engine_error_type = error_type
        self._error_message = message
