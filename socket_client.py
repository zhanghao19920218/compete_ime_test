#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : haozhang45@iflytek.com
# @Time    : 2021/10/15 19:19
# @File    : socket_client.py
import json
import os
import socket
import time

from typing.io import TextIO

from Model.device_utils_model import DeviceUtilsModel
from Parameter import InputCom, Parameter
from appium_section.ba_adb import BAADB
from appium_section.baappiumutils import BAAppiumUtils
from appium_section.models.config_reader import DeviceModel, ConfigReader

input_format_str = "{\"cmd\" : \"commit\", \"params\" : { \"out_put_type\":{out_put_type},\"index\": {index} }"
query_str = "{\"cmd\":\"query\"}"
reset_str = "{\"cmd\":\"reset\"}"
catch_user_word_str = "{\"cmd\":\"set_user_word_count\"}"
user_word_str = "{\"cmd\":\"get_user_word_count\"}"
last_str = "{\"cmd\":\"pressed_last\"}"


class ImeHookSocket(object):
    """
    Ime Hook 的Socket链接
    """
    adb_path: str
    local_port: int
    remote_port: int
    device_name: str

    def __init__(self,
                 device_name: str,
                 adb_path: str = "adb",
                 local_port: int = 9999,
                 remote_port: int = 2000):
        self.adb_path = adb_path
        self.device_name = device_name
        # 重置adb
        os.system('%s kill-server' % self.adb_path)
        os.system('%s devices' % self.adb_path)
        # 连接虚拟机
        os.system('%s connect %s' % (self.adb_path, self.device_name))
        # 映射虚拟机端口到主机端口
        os.system(
            '%s -s %s forward tcp:%s tcp:%s' % (self.adb_path, self.device_name, self.local_port, self.remote_port))

    def get_devices(self):
        os.system('%s devices' % self.adb_path)


def socket_ime(simulator_port: str,
               parameter: Parameter,
               device_index: int,
               brand_type: InputCom) -> socket:
    """
    链接虚拟adb
    :param simulator_port:
    :param parameter: 输入参数
    :param brand_type: 输入法名称
    :param device_index: 设备的名称
    :return:
    """
    # 连接虚拟机adb
    # adb_con: BAADB = BAADB(device_name=device_name)
    # adb_con.connect_device()
    # 启动IMEHook
    # time.sleep(5)
    # adb_con.kill_apk()  # 先杀死应用
    ba_appium_utils = DeviceUtilsModel.shared(index=device_index).devices_appium_ms
    device_name: str = DeviceUtilsModel.shared(index=device_index).devices_models[device_index].deviceName
    ba_appium_utils.start_app()
    ba_appium_utils.set_ime_keyboard(ime_type=brand_type)
    time.sleep(5)
    ba_appium_utils.get_input_text_view()
    time.sleep(5)
    ba_appium_utils.change_menu(key_board_brand=parameter.ime_type,
                                key_board_type=parameter.ime_keyboard_type,
                                is_english=False)
    # 映射虚拟机端口到主机端口
    # sock: socket = adb_con.create_connection(socket_port=int(simulator_port))
    # adb_con.socket_shell(socket_port=int(simulator_port))
    os.system(f'adb -s {device_name} forward tcp:9999 tcp:' + simulator_port)
    # 切换输入法
    # 启动IMEHook
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9999))
    return sock


def socket_ime_appium(simulator_port: str,
                      device_name: str) -> socket:
    """
    new socket ime in appium to get detail information
    :param simulator_port: send socket in which port
    :param device_name: device name for real device
    :return:
    """
    # 映射虚拟机端口到主机端口
    os.system(f'adb -s {device_name} forward tcp:9999 tcp:' + simulator_port)
    # 切换输入法
    # 启动IMEHook
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9999))
    return sock


def socket_close(sock):
    sock.close()


def socket_input(sock: socket,
                 sock_file: TextIO) -> str:
    """
    获取socket结果
    :param sock:
    :param sock_file:
    :return:
    """
    sock.send((query_str + '\n').encode('utf-8'))
    result = sock_file.readline()
    return result


def socket_associate(sock: socket,
                     sock_file: TextIO) -> str:
    """
    获取联想词
    :param sock:
    :param sock_file:
    :return:
    """
    sock.send((query_str + '\n').encode('utf-8'))
    result = sock_file.readline()
    return result


def reset_input(sock, sock_file):
    sock.send((reset_str + '\n').encode('utf-8'))
    sock_file.readline()


def send_upper_screen_request(sock: socket,
                              sock_file: TextIO,
                              index: int,
                              upper_screen_type: bool):
    """
    index 选候选词
    :param sock:
    :param sock_file:
    :param index:
    :param upper_screen_type: true全匹配时直接上屏结果， false 半匹配时多次上屏
    :return:
    """
    temp_obj: dict = {"cmd": "commit"}
    params_obj: dict = {"out_put_type": upper_screen_type, "index": index}
    temp_obj["params"] = params_obj
    sock.send((json.dumps(temp_obj) + '\n').encode('utf-8'))
    sock_file.readline()


def compose_target_word(sock: socket,
                        sock_file: TextIO,
                        target_word: str):
    """
    提交需要选词的目标词汇
    :param sock:
    :param sock_file:
    :param target_word:
    :return:
    """
    temp_obj: dict = {"cmd": "target_word"}
    params_obj: dict = {"word": target_word}
    temp_obj["params"] = params_obj
    sock.send((json.dumps(temp_obj) + '\n').encode('utf-8'))
    sock_file.readline()


def compose_last_word(sock: socket,
                      sock_file: TextIO):
    """
    Composing the last word
    :param sock:
    :param sock_file:
    :return:
    """
    sock.send((last_str + '\n').encode('utf-8'))
    sock_file.readline()

def catch_user_words_dict(sock: socket,
                          sock_file: TextIO) -> str:
    """
    触发获取用户词数量
    :param sock:
    :param sock_file:
    :return:
    """
    sock.send((catch_user_word_str + '\n').encode('utf-8'))
    result = sock_file.readline()
    return result


def get_user_word_count(sock: socket,
                        sock_file: TextIO) -> str:
    """
    获取用户词的数量结果
    :param sock:
    :param sock_file:
    :return:
    """
    sock.send((user_word_str + '\n').encode('utf-8'))
    result = sock_file.readline()
    return result
