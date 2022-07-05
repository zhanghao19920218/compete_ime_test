# -*- coding:utf-8 -*-
# @Time : 2021/09/12 15:29
# @Author : haozhang45
# @TODO : 定制输入参数
import socket
from typing import List
from typing.io import TextIO
from enum import Enum


class TestType(Enum):
    """
    测试的内容
    Decode 解码,联想, 云端
    CloudLost 云端丢失
    NameType 人名模式
    ConnectionType 上下文属性
    """
    Decode = 1  # 解码类型
    CloudLost = 2  # 云端丢失
    NameType = 3  # 人名模式
    ConnectionType = 4  # 上下文属性


class ErrorInfoType(Enum):
    """
    分步选词的解码错误
    """
    DecodeError = 1  # 解码错误
    OverflowStep = 2  # 超出选词长度错误
    Success = 3  # 获取结果成功


class OutPutType(Enum):
    """
    输出文件的内容
    """
    Local = 1  # 本地
    Cloud = 2  # 云端
    Correct = 3  # 纠错


class InputCom(Enum):
    """
    选择的输入法厂家
    """
    Sogou = 1  # 搜狗输入法
    IflyTek = 2  # 讯飞输入法
    Baidu = 3  # 百度输入法
    IflytekReal = 4  # 真机讯飞输入法


class KeyboardType(Enum):
    """
    输入键盘的类型: 26key还是9key
    """
    Keyboard26Key = 1  # 26键
    Keyboard9Key = 2  # 9键


class FileReadType(Enum):
    """
    文件读取类型
    line_special  py    word:result
    piece
        input：pingyin
        iflytek_candi:***
    """
    Line = 0  # 按行读取
    Piece = 1  # 按块读取
    SpecialLine = 3  # 特殊行


class Parameter:
    # 基础信息部分
    # 输入法类型 "Sogou"  "Iflytek"
    ime_type: InputCom = InputCom.Sogou  # 默认搜狗

    # 键盘类型
    ime_keyboard_type: KeyboardType = KeyboardType.Keyboard26Key

    # 抓取结果输出类型 1:"local", 2:"cloud", 3:"correct"
    output_type: List[OutPutType] = [OutPutType.Local]

    # 抓取文件路径
    input_file_path: str = ""

    # 文件数据读取类型  "line", "piece", 默认设置为"line"
    input_date_item_type: FileReadType = FileReadType.Line

    # line 类型 split 读取位置
    line_type_word_index: int = 0
    line_type_sound_index: int = 0

    # 模拟器部分信息
    # 模拟器IMEHook进程ID
    simulator_process_id: str = ""

    # socket部分信息
    # socket交互对象
    sock: socket = None
    # socket数据读取
    sock_file: TextIO = None

    # 抓取进度信息
    # 进度位置
    speed_of_progress: dict = {}

    # 基础数据
    # 单个文件数据
    file_data: list = []

    # 是否需要每一步匹配解码
    is_need_match_step_decode: bool = False

    # 是否需要检测网络
    is_need_check_network: bool = False

    # 是否需要时间戳
    is_need_time_stamp: bool = False

    # 是否开启三步选词机制
    is_pick_three_step_sys: bool = False

    # 测试的类型
    test_type: TestType = TestType.Decode

    # 是否需要展开结果
    is_need_open: bool = False

    # 是否需要测试用户词数量
    is_need_user_word_count: bool = False

    def is_not_iflytek(self) -> bool:
        """
        是否是讯飞输入法
        :return:
        """
        return self.ime_type == InputCom.Baidu or self.ime_type == InputCom.Sogou

    def __init__(self, ime_type: InputCom,
                 ime_keyboard_type: KeyboardType,
                 output_type: List[OutPutType],
                 input_file_path: str,
                 is_need_check_net: bool,
                 input_date_item_type: FileReadType,
                 is_need_time_stamp: bool,
                 is_need_match_step_decode: bool,
                 is_need_open: bool,
                 is_need_user_word_count: bool,
                 is_pick_three_step_sys: bool):
        """
        初始化输入模式参数
        :param ime_type:
        :param ime_keyboard_type:
        :param output_type:
        :param input_file_path:
        :param input_date_item_type:
        :param is_need_match_step_decode: 是否需要一步一步解码获取
        :param is_need_time_stamp: 是否需要时间戳
        :param is_need_user_word_count: 是否需要用户词语
        """
        self.ime_type = ime_type
        self.ime_keyboard_type = ime_keyboard_type
        self.output_type = output_type
        self.input_file_path = input_file_path
        self.input_date_item_type = input_date_item_type
        self.is_need_match_step_decode = is_need_match_step_decode
        self.is_need_check_network = is_need_check_net
        self.is_need_time_stamp = is_need_time_stamp
        self.is_pick_three_step_sys = is_pick_three_step_sys
        self.is_need_open = is_need_open
        self.is_need_user_word_count = is_need_user_word_count

    def __init_socket__(self, socket_inner: socket, socket_file: TextIO):
        """
        初始化Socket链接
        :param socket_inner: web_socket创建
        :param socket_file:
        :return:
        """
        self.sock = socket_inner
        self.sock_file = socket_file
