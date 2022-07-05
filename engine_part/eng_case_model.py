# coding=utf-8
# @author: haozhang45
# @date: 2022/3/21
# @description: 解析引擎测试集
import time
from socket import socket

from Model.ReturnTypeModel import ReturnTypeModel
from Parameter import InputCom
from appium_section.baappiumutils import BAAppiumUtils
from appium_section.models.config_reader import DeviceModel
from eng_interface import EngineInterface
from engine_part.engine_mappy import EngineMethod, EngineKeyboardType, EngineInputType, FuzzyType
from typing import List, TextIO
from error.error_model import EngineTCError, EngineErrorEnum
from Parameter import KeyboardType
from input import write_keyboard_input, delete_upper_screen_result
from server import update_json
from socket_client import socket_ime_appium, socket_input, send_upper_screen_request


class EngineCaseModel(EngineInterface):
    """
    引擎初始化model
    """
    _engine_method_dict: dict

    _keyboard_brand: InputCom

    _keyboard_type: KeyboardType

    _tmp_word: str  # temporary word, replace in write method

    _socket: socket = None

    _socket_file: TextIO = None

    _device_model: DeviceModel = None

    _ba_appium_util: BAAppiumUtils = None

    _candidates_list: List[str] = []

    _associate_list: List[str] = []

    @property
    def engine_method_dict(self) -> dict:
        return self._engine_method_dict

    def __init__(self,
                 keyboard_brand: InputCom,
                 device_model: DeviceModel):
        self._keyboard_brand = keyboard_brand
        self._engine_method_dict: dict = {
            EngineMethod.INIT_ENGINE: self.init_engine,
            EngineMethod.SWAP_METHOD: self.swap_method,
            EngineMethod.INPUT_KEYS_RANDOM: self.input_keys,
            EngineMethod.INPUT_KEYS: self.input_keys,
            EngineMethod.GET_WORDS: self.get_words,
            EngineMethod.SELECT_WORD: self.select_word,
            EngineMethod.RESET: self.reset_engine,
            EngineMethod.RELEASE_ENGINE: self.release_engine,
            EngineMethod.GET_ASSOCIATE: self.get_associate,
            EngineMethod.DELETE: self.delete_pinyin,
        }
        self._device_model = device_model
        self._ba_appium_util = BAAppiumUtils(model=device_model)

    def reset_socket(self,
                     device_name: str):
        """
        rebuild a socket connection
        :param device_name: device name for device
        :return:
        """
        # first judge socket is whether exist
        if self._socket is not None:
            self._socket.close()
        if self._socket_file is not None:
            self._socket_file.close()
        if self._keyboard_brand == InputCom.Sogou:
            # sogou ime keyboard
            simulator_port = "9999"
        elif self._keyboard_brand == InputCom.Baidu:
            # baidu ime keyboard
            simulator_port = "9999"
        else:
            simulator_port = "8888"
        # create socket
        self._socket = socket_ime_appium(simulator_port=simulator_port,
                                         device_name=device_name)
        self._socket_file = self._socket.makefile(encoding='utf-8')

    def init_engine(self,
                    param: str = ""):
        """
        初始化引擎
        :return:
        """
        print("引擎初始化")
        self._ba_appium_util.start_app()
        self._ba_appium_util.set_ime_keyboard(ime_type=self._keyboard_brand)
        time.sleep(5)
        self._ba_appium_util.get_input_text_view()
        # restart socket ime
        self.reset_socket(device_name=self._device_model.deviceName)
        time.sleep(5)

    def swap_method(self,
                    method_name: str = ""):
        """
        swap engine method
        :param method_name: get engine method name
        :return:
        """
        print("切换方法")
        print(method_name)
        method_details_types: List[str] = method_name.split(" ")
        if len(method_details_types) < 2:
            raise EngineTCError(error_type=EngineErrorEnum.SWAP_METHOD_ERROR,
                                message="Swap methods needs more than two parameters")  # throw swap method error
        elif len(method_details_types) == 2:
            keyboard_type: EngineKeyboardType = EngineKeyboardType(
                value=method_details_types[0])  # get engine keyboard type: 26key or 9key
            input_type: EngineInputType = EngineInputType(
                value=method_details_types[1])  # get engine input type: english or pinyin
            fuzzy_model: FuzzyType = FuzzyType.NO_FUZZY_KEY  # fuzzy type: fuzzy key or fuzzy pinyin or none
        else:
            keyboard_type: EngineKeyboardType = EngineKeyboardType(
                value=method_details_types[0])  # get engine keyboard type: 26key or 9key
            input_type: EngineInputType = EngineInputType(
                value=method_details_types[1])  # get engine input type: english or pinyin
            fuzzy_model: FuzzyType = FuzzyType(
                value=method_details_types[2])  # fuzzy type: fuzzy key or fuzzy pinyin or none
        # According parameters to run start
        # Change English or Pinyin
        self._keyboard_type = KeyboardType.Keyboard9Key if keyboard_type == EngineKeyboardType.NINE_KEY_BOARD else KeyboardType.Keyboard26Key
        # self._ba_appium_util.change_menu(key_board_brand=self._keyboard_brand,
        #                                  key_board_type=self._keyboard_type,
        #                                  is_english=input_type == EngineInputType.EN)
        # self._ba_appium_util.wait_seconds(seconds=0.5)
        # # Is Fuzzy Or Not
        # # setting more keyboard
        # self._ba_appium_util.menu_setting(key_board_brand=self._keyboard_brand)
        # # setting fuzzy type
        # self._ba_appium_util.check_is_fuzzy(set_fuzzy=fuzzy_model == FuzzyType.FUZZY_KEY)
        # # click pop back button to main app
        # self._ba_appium_util.back_action()
        # self._ba_appium_util.back_action()
        # click text view to pop keyboard
        self._ba_appium_util.get_input_text_view()

    def input_keys(self,
                   input_str: str = ""):
        """
        input word characters
        :param input_str: input random string
        :return:
        """
        write_keyboard_input(word_code=input_str,
                             appium_utils=self._ba_appium_util,
                             keyboard_type=self._keyboard_type,
                             keyboard_brand=self._keyboard_brand)
        self._tmp_word = input_str
        # print(input_str)
        # print("输入按键")

    def get_words(self,
                  param: str = ""):
        """
        Get decodes candidates
        :return:
        """
        time.sleep(0.5)
        # get candidates of diff brand apk
        return_socket_str: str = socket_input(sock=self._socket,
                                              sock_file=self._socket_file)
        if return_socket_str is not None:
            model: ReturnTypeModel = update_json(return_socket_str=return_socket_str,
                                                 ime_type=self._keyboard_brand)
            self._candidates_list = model.candidate_list
            print(model.candidate_list)
            # decode_return_model.candidate_list = model.candidate_list
            # # 获取云端解码结果
            # decode_return_model.cloud_list = model.cloud_list
            # # 获取原始解码数据
            # decode_return_model.origin_json_str = model.origin_json

    def delete_pinyin(self,
                      param: str = ""):
        self._ba_appium_util.delete_action(key_board_brand=self._keyboard_brand,
                                           key_board_type=self._keyboard_type)

    def reset_engine(self,
                     param: str = ""):
        """
        重置输入
        :return:
        """
        # delete_upper_screen_result(keyboard_type=self._keyboard_type,
        #                            keyboard_brand=self._keyboard_brand,
        #                            word_len=len(self._tmp_word),
        #                            appium_util=self._ba_appium_util)
        self._ba_appium_util.clear_button_action(key_board_brand=self._keyboard_brand)

    def release_engine(self,
                       param: str = ""):
        """
        释放引擎
        :return:
        """
        print("释放引擎")

    def select_word(self,
                    param: str = ""):
        """
        选词
        :return:
        """
        # print("选词")
        # if param in self._candidates_list:
        #     select_index: int = self._candidates_list.index(param)
        #     # 如果选词在列表里面，就进行选词
        #     send_upper_screen_request(sock=self._socket,
        #                               sock_file=self._socket_file,
        #                               index=select_index,
        #                               upper_screen_type=True)
        # else:
        #     print("没有选词成功")
        self._ba_appium_util.choose_word(key_board_brand=self._keyboard_brand)

    def get_associate(self,
                      param: str = ""):
        """
        获取选词
        :return:
        """
        print("联想结果")
        print(param)
        return_socket_str: str = socket_input(sock=self._socket,
                                              sock_file=self._socket_file)
        if return_socket_str is not None:
            model: ReturnTypeModel = update_json(return_socket_str=return_socket_str,
                                                 ime_type=self._keyboard_brand)
            self._associate_list = model.candidate_list
            print(self._associate_list)
