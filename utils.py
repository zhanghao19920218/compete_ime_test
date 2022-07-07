# coding: utf-8
# 新增处理的工具类
import os
import re
import subprocess
import time
import multiprocessing as mp
from threading import Thread
from subprocess import call

# from Model.FrontWindow import FrontWindow
import warnings
from time import sleep

# def clicked_left_mouse():
#     """
#     处理鼠标自动点击屏幕, 重启防止各种系统弹窗
#     :return:
#     """
#     # 屏幕分辨率
#     # screen_size: Size = pyautogui.size()
#     # 鼠标位置
#     # mouse_pos: Point = pyautogui.position()
#     # 点击一下当前位置
#     pyautogui.click(button="left")


# def move_mumu_to_front():
#     """
#     移动Mumu模拟器到最前端
#     :return:
#     """
#     sleep(5)
#     try:
#         regex = ".*MuMu模拟器*"
#         cW = FrontWindow()
#         cW.find_window_regex(regex)
#         # 页面最大化
#         # cW.Maximize()
#         cW.SetAsForegroundWindow()
#     except:
#         print("Mumu模拟器移动到最前端失败")
from typing import List

from Parameter import Parameter, InputCom


def create_time_stamp() -> str:
    """
    获取时间戳
    :return:
    """
    millis = int(round(time.time() * 1000))
    return f"{millis}"


def socket_create_by_(socket_parameter: Parameter,
                      iflytek_port: int) -> str:
    """
    初始化socket参数
    :param socket_parameter:
    :param device_index: 设备的index
    :return: return socket string
    """
    if socket_parameter.sock is not None:
        socket_parameter.sock.close()
    if socket_parameter.sock_file is not None:
        socket_parameter.sock_file.close()
    if socket_parameter.ime_type == InputCom.Sogou:
        # 搜狗输入法创建socket
        simulator_port = "9999"
    elif socket_parameter.ime_type == InputCom.Baidu:
        # 百度输入法创建socket
        simulator_port = "9999"
    else:
        simulator_port = f"{iflytek_port}"
    return simulator_port


def kill_port_process(ports: List[str]):
    """
    关闭port进程
    :param ports:
    :return:
    """
    warnings.warn("kill_port_process is deprecated", DeprecationWarning)
    popen = subprocess.Popen(['netstat', '-lpn'],
                             shell=False,
                             stdout=subprocess.PIPE,
                             encoding='utf-8')
    (data, err) = popen.communicate()

    pattern = "^tcp.*((?:{0})).* (?P<pid>[0-9]*)/.*$"
    pattern = pattern.format(')|(?:'.join(ports))
    prog = re.compile(pattern)
    for line in data.split('\n'):
        match = re.match(prog, line)
        if match:
            pid = match.group('pid')
            subprocess.Popen(['kill', '-9', pid])


def run_multiprocess(func, parameters):
    """
    运行多进程
    :param func:
    :param parameters:
    :return:
    """
    warnings.warn("run_multiprocess deprecated", DeprecationWarning)
    # Parallelize using Pool.apply()
    # Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())

    # Step 2: `pool.apply` the `func`
    results = [pool.apply_async(func, args=(row["index"], row["type"])) for row in parameters]

    # Step 3: Don't forget to close
    pool.close()
    pool.join()


def run_command_line(command: str):
    """
    run single core command
    :param command:
    :return:
    """
    call(command, shell=True)


def run_multicore(command: str,
                  python_file: str,
                  parameters: List[int]):
    """
    Run multi testcase by multi cores
    :param command: python3、python2
    :param python_file: python file
    :param parameters:
    :return:
    """
    # Step 1: set the parameters
    for parameter in parameters:
        print(parameter)
        print(f"command line: {command} {python_file} {parameter}")
        thread = Thread(target=run_command_line, args=[f"{command} {python_file} {parameter}"])
        thread.start()


def pinyin_to_num(pinyin: str) -> str:
    """
    拼音转为数字
    :param pinyin:
    :return:
    """
    ret: str = ""
    for single_item in pinyin:
        ret += f"{single_alpha_to_num(alpha=single_item)}"
    return ret


def single_alpha_to_num(alpha: str) -> int:
    """
    单独的汉字转为数字
    :param alpha:
    :return:
    """
    if alpha in 'abc':
        return 2
    elif alpha in 'def':
        return 3
    elif alpha in 'ghi':
        return 4
    elif alpha in 'jkl':
        return 5
    elif alpha in 'mno':
        return 6
    elif alpha in 'pqrs':
        return 7
    elif alpha in 'tuv':
        return 8
    elif alpha in 'wxyz':
        return 9
