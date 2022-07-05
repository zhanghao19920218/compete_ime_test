# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
from appium_section.models.config_reader import DeviceModel

from appium_section.baappiumutils import BAAppiumUtils
from ime_constant import IME_Constant
from Parameter import KeyboardType, Parameter, InputCom

log_path = 'logs'
input_path = 'py_dict.100w.sort_freq.txt'

input_key_delay = 0.0200
input_key_delay1 = 0.1
input_switch_delay = 0.2
input_line_delay = 0.02
epoch_len = 1000
# 等待云端结果的时间
wait_cloud_word_delay = 1


def single_word_pick_result(ime_type: InputCom,
                            appium_util: BAAppiumUtils):
    """
    长按获取下拉候选词
    :param ime_type: 输入法的类型
    :param appium_util: Appium的点击方式
    :return: 选择了单字选词
    """
    time.sleep(0.5)
    appium_util.down_arrow_action(key_board_brand=ime_type)
    for_times: int = 5
    time.sleep(0.5)
    if ime_type == InputCom.Baidu:
        for _ in range(for_times):
            appium_util.press_baidu_next_page()
            time.sleep(0.2)


def down_arrow_pressed(ime_type: InputCom,
                       appium_util: BAAppiumUtils):
    """
    点击关闭更多候选词, 向上箭头 强制
    :param ime_type: 是搜狗还是讯飞输入法
    :param appium_util: Appium的model
    :return:
    """
    appium_util.down_arrow_action(key_board_brand=ime_type)
    time.sleep(0.5)
    appium_util.down_arrow_action(key_board_brand=ime_type)


def back_line_candidate(ime_type: InputCom,
                        appium_util: BAAppiumUtils):
    """
    返回单行解码结果
    :param ime_type:
    :param appium_util:
    :return:
    """
    appium_util.back_line_action(key_board_brand=ime_type)


def force_cloud(pid):
    time.sleep(0.5)
    # 向上箭头 强制
    # win32api.SendMessage(pid, win32con.WM_KEYDOWN, 38, 0)
    # win32api.SendMessage(pid, win32con.WM_KEYUP, 38, 0)
    time.sleep(0.5)


def delete_upper_screen_result(keyboard_brand: InputCom,
                               keyboard_type: KeyboardType,
                               word_len: int,
                               appium_util: BAAppiumUtils):
    """
    delete upper screen pinyin
    :param keyboard_brand get the company name of ime keyboard
    :param keyboard_type: get the type of keyboard: 26key or 9key
    :param word_len word characters length
    :param appium_util
    :return:
    """
    appium_util.delete_action(key_board_brand=keyboard_brand,
                              key_board_type=keyboard_type,
                              duration_time=200 * word_len)
    time.sleep(0.5)


def clear_button_action(parameter: Parameter,
                        ba_appium_util: BAAppiumUtils):
    """
    点击清空输入框内容
    :param parameter:
    :param ba_appium_util
    :return:
    """
    ba_appium_util.clear_button_action(key_board_brand=parameter.ime_type)


def enter_blank_space(parameter: Parameter,
                      ba_appium_util: BAAppiumUtils):
    """
    点击回车按钮
    :param parameter: 输入参数
    :param ba_appium_util: BAAppiumUtils
    :return:
    """
    ba_appium_util.choose_word(key_board_brand=parameter.ime_type)
    time.sleep(1)


def write_keyboard_input(word_code: str,
                         appium_utils: BAAppiumUtils,
                         keyboard_brand: InputCom,
                         keyboard_type: KeyboardType):
    """
    根据虚拟键盘输入单字
    :param word_code: 解码所需要英文字母
    :param appium_utils: Appium Utils Model
    :param keyboard_brand: get the company name of ime keyboard
    :param keyboard_type: get the type of keyboard: 26key or 9key
    :return:
    """
    appium_utils.write_string(word=word_code,
                              key_board_brand=keyboard_brand,
                              keyboard_type=keyboard_type)
    time.sleep(wait_cloud_word_delay)


def press_last_word_pos(keyboard_brand: InputCom,
                        ba_appium_util: BAAppiumUtils):
    """
    点击最后上屏的解码结果
    :param keyboard_brand:
    :param ba_appium_util: Appium的utils
    :return:
    """
    ba_appium_util.press_last_word(key_board_brand=keyboard_brand)
    time.sleep(0.3)


def hide_keyboard(ba_appium_util: BAAppiumUtils):
    """
    收起键盘
    :param ba_appium_util: BAAppiumUtils
    :return:
    """
    ba_appium_util.hide_keyboard()


def pop_keyboard(ba_appium_util: BAAppiumUtils):
    """
    弹出键盘
    :return:
    """
    if not ba_appium_util.is_show_keyboard():
        ba_appium_util.get_input_text_view()


def wait_for_keyboard():
    """
    设置睡眠时间
    :return:
    """
    time.sleep(2)


def pressed_enter(keyboard_brand: InputCom,
                  ba_appium_util: BAAppiumUtils):
    """
    点击回车按钮
    :param keyboard_brand:
    :param ba_appium_util: 设备
    :return:
    """
    ba_appium_util.pressed_enter_button(key_board_brand=keyboard_brand)


def enter_name_model_button(parameter: Parameter):
    """
    点击人名模式按钮
    :param parameter: 点击进入人名模式
    :return:
    """
#     press_keyboard(pid=parameter.simulator_process_id,
#                    key=0xDC)
#     time.sleep(input_key_delay)
#     time.sleep(0.2)
#     win32api.SendMessage(parameter.simulator_process_id, win32con.WM_KEYDOWN, win32con.VK_UP, 0)
#     time.sleep(IME_Constant.IME_NAME_MODE_KEY_UP_TIME)
#     win32api.SendMessage(parameter.simulator_process_id, win32con.WM_KEYUP, win32con.VK_UP, 0)


# def set_mouse_click(hwnd, x_coord, y_coord):
#     SetForegroundWindow(hwnd)
#     win32api.SetCursorPos([int(x_coord), int(y_coord)])
#     # 执行左单键击，若需要双击则延时几毫秒再点击一次即可
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


# def save_check_point(pid, num_epoch, last_offset):
#     os.system('adb -s %s shell /system/bin/screencap -p /sdcard/screenshot_%s.png' % (DevicesID, num_epoch))  # 保存在手机中
#     os.system('adb -s %s pull /sdcard/screenshot_%s.png SougouSmart/screenshot_%s.png' % (
#         DevicesID, num_epoch, num_epoch))  # 导入PC端
#     with open('SougouSmart/word_%s.log' % num_epoch, 'w', encoding='utf-8') as f:
#         with open(log_path, 'r', encoding='utf-8') as log:
#             log.seek(last_offset, 0)
#             while True:
#                 line = log.readline()
#                 if line:
#                     f.write(line)
#                 else:
#                     break
#             cur_offset = log.tell()
#
#     win32api.SendMessage(pid, win32con.WM_KEYDOWN, win32con.VK_LEFT, 0)
#     win32api.SendMessage(pid, win32con.WM_KEYUP, win32con.VK_LEFT, 0)
#     time.sleep(input_key_delay)
#
#     for _ in range(100):
#         win32api.SendMessage(pid, win32con.WM_KEYDOWN, win32con.VK_DOWN, 0)
#         win32api.SendMessage(pid, win32con.WM_KEYUP, win32con.VK_DOWN, 0)
#         time.sleep(input_key_delay)
#
#     return cur_offset


# def remove_one_char(parameter: Parameter):
#     """
#     回删一位
#     :param parameter: 输入参数
#     :return:
#     """
#     press_keyboard(parameter.simulator_process_id,
#                    IME_Constant.IME_KEYBOARD_BACKSPACE)
#     time.sleep(input_key_delay)
#
#
# def write_keyboard_last_char(ascii_code: str,
#                              parameter: Parameter):
#     """
#     根据虚拟键盘输入单字
#     :param ascii_code: 解码所需要英文字母
#     :param parameter: 输入参数
#     :return:
#     """
#     press_keyboard(parameter.simulator_process_id, ascii_code)
#     time.sleep(input_key_delay)
