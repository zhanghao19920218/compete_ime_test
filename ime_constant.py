# -*- coding:utf-8 -*-
# @Time : 2019/7/15 13:45 
# @Author : haozhang45
# @TODO : 系统中使用的常量

class IME_Constant:

    # 点击回车按钮
    IME_KEYBOARD_RETURN = 13
    # 回删按钮
    IME_KEYBOARD_BACKSPACE = 8

    # 按键时间的设置, 根据不同的电脑配置可能需要修改
    IME_COMMIT_DELAY_TIME = 2

    # 重启socket延迟
    IME_REBOOT_SOCKET = 1

    # 没有云端结果可以启动次数
    IME_REBOOT_SOCKET_TIMES = 0

    # 判断是否要选词
    IME_NEED_COMMIT_STR = "####"

    # 长按上面箭头的延迟，来回去下拉菜单候选词, 一般选2,多于2选词位置会报错
    IME_LONG_PRESS_KEY_UP_TIME = 2

    # 长按上面箭头的延迟，来回去下拉菜单候选词, 一般选2,多于2选词位置会报错
    IME_NAME_MODE_KEY_UP_TIME = 2

    # 云端丢失文件名
    CLOUD_LOST_FILE: str = "cloud_lose_file.txt"