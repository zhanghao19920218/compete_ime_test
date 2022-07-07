#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : haozhang45@iflytek.com
# @Time    : 2021-03-11 11:33
# @File    : main.py
import sys
from typing import Tuple
from goto import with_goto
from dominate.tags import label
import goto
import socket_client
import server
import datetime
from error.error_model import AppiumError, EmulatorError
from file_io import *
from input import *
from Parameter import *
from test_api_part.cloud_api_util import run_service_cloud
from name_function.name_func import run_name_service
from connection_function.connection_fun_part import run_connection_service
from utils import socket_create_by_, run_multicore


def get_socket_by_IME_type(inner_parameter: Parameter,
                           device_index: int):
    """
    创建Socket
    :param inner_parameter:
    :param device_index: 设备的index
    :return: 返回创建的socket参数
    """
    # 首先判断Socket文件和链接是否存在, 不存在就重新构建
    simulator_port: str = socket_create_by_(socket_parameter=inner_parameter,
                                            iflytek_port=DeviceUtilsModel.shared(index=device_index).devices_models[
                                                device_index].iflytekPort)
    # 创建socket
    inner_parameter.sock = socket_client.socket_ime(simulator_port=simulator_port,
                                                    parameter=inner_parameter,
                                                    brand_type=inner_parameter.ime_type,
                                                    device_index=device_index)
    inner_parameter.sock_file = inner_parameter.sock.makefile(encoding='utf-8')


def get_index_info(temp_info_dict: dict) -> Tuple[int, str, list]:
    """
    获取每一行的信息, 然后返回每一个子信息
    :param temp_info_dict: 获取加载的信息
    :return:
    """
    index = 0
    client_file = ""
    completed_grab_file_list = []
    if "index" in temp_info_dict:
        index = temp_info_dict["index"]
        client_file = temp_info_dict["client_file"]
        completed_grab_file_list = temp_info_dict["complete_file"]
    else:
        temp_info_dict["index"] = 0
        temp_info_dict["client_file"] = ""
        temp_info_dict["total_count"] = 0
        temp_info_dict["complete_file"] = []
    return index, client_file, completed_grab_file_list


@with_goto
def main(parameter_inner: Parameter,
         device_index: int):
    """
    主函数
    :param parameter_inner: 输入模式
    :param device_index: 设备的index
    :return:
    """
    # 定义临时索引JSONObject
    # 获取socket，通过IME_type进行区分创建
    label.begin
    get_socket_by_IME_type(parameter_inner,
                           device_index=device_index)
    # 获取待抓取文件列表
    stay_grab_file_list = os.listdir(parameter_inner.input_file_path)
    # 获取模拟器窗口pid
    # init_simulate(parameter_inner)
    # 点击一下鼠标左键
    # clicked_left_mouse()
    # 获取抓取结果进度
    parameter_inner.speed_of_progress = get_temp_file_info(device_index=device_index)
    index, client_file, completed_grab_file_list = get_index_info(parameter_inner.speed_of_progress)

    for i in range(0, len(stay_grab_file_list)):
        path = os.path.join(parameter_inner.input_file_path, stay_grab_file_list[i])
        if os.path.isfile(path) and path.endswith(".txt"):
            parameter_inner.file_data = get_current_data(path=path,
                                                         read_type=parameter_inner.input_date_item_type)
            if stay_grab_file_list[i] in completed_grab_file_list:
                print("{file_path} 数据已抓取完成！".format(file_path=path))
                continue
            else:
                if "index" in parameter_inner.speed_of_progress:
                    parameter_inner.speed_of_progress["client_file"] = stay_grab_file_list[i]
                    parameter_inner.speed_of_progress["total_count"] = len(parameter_inner.file_data)
                start = datetime.datetime.now()
                try:
                    # 捕获运行的异常进行重新运行
                    if parameter_inner.test_type == TestType.NameType:
                        # 人名模式
                        run_name_service(parameter=parameter_inner)
                    elif parameter_inner.test_type == TestType.ConnectionType:
                        # 上下文模式
                        run_connection_service(parameter=parameter_inner,
                                               device_index=device_index)
                    else:
                        # 解码, 选词, 联想词模式
                        server.run_service(parameter=parameter_inner,
                                           device_index=device_index)
                except EmulatorError as emulatorError:
                    print(emulatorError.message)
                    time.sleep(IME_Constant.IME_REBOOT_SOCKET)
                    goto.begin
                except AppiumError as appiumError:
                    print(appiumError.message)
                    time.sleep(IME_Constant.IME_REBOOT_SOCKET)
                    goto.begin

                end = datetime.datetime.now()
                print("{file}执行时长:{time}".format(file=stay_grab_file_list[i], time=end - start))

                completed_grab_file_list.append(stay_grab_file_list[i])
                parameter_inner.speed_of_progress["client_file"] = ""
                parameter_inner.speed_of_progress["total_count"] = 0
                parameter_inner.speed_of_progress["index"] = 0
                parameter_inner.speed_of_progress["complete_file"] = completed_grab_file_list
                set_temp_file_info(current_dict=parameter_inner.speed_of_progress,
                                   device_index=device_index)


def catch_cloud_action(parameter_inner: Parameter):
    """
    抓取云端数据丢失率
    :param parameter_inner: 输入模式
    :return:
    """
    # 定义临时索引JSONObject
    # 获取socket，通过IME_type进行区分创建
    get_socket_by_IME_type(parameter_inner)
    # 获取模拟器窗口pid
    # init_simulate(parameter_inner)
    # 捕获运行的异常进行重新运行
    run_service_cloud(parameter=parameter_inner)


def old_ime_test(device_id: int):
    """
    老版本按键测试
    :return:
    """
    # 清除之前抓取的内容
    # clear_file()
    # 输入类型 `Sogou` `IflyTek`
    ime_type: InputCom = DeviceUtilsModel.shared(index=device_id).devices_models[device_id].ime_type
    # 键盘类型 "" "26k"
    keyboard_type: KeyboardType = DeviceUtilsModel.shared(index=device_id).devices_models[device_id].keyboard_type
    # 抓取结果类型 1:"local" 2:"cloud" 3:"correct"
    output_type: List[OutPutType] = [OutPutType.Local, OutPutType.Cloud]
    # 抓取文件路径
    input_path_doc: str = os.getcwd() + f"/test/{DeviceUtilsModel.shared(index=device_id).devices_models[device_id].read_file_path}"
    # 文件输入格式 单条数据格式 "line" "piece" "line_special"
    input_date_item_type: FileReadType = FileReadType.Line
    # 是否需要自动补全位置
    is_need_step_decoded: bool = True
    # 是否需要检测网络状态
    is_need_check_net: bool = False
    # 是否需要时间戳
    is_need_time_stamp: bool = False
    # 是否开启三步选词功能git
    is_three_steps_open: bool = False
    # 是否测试云端丢失率, ConnectionType是上下文属性
    test_type: TestType = DeviceUtilsModel.shared(index=device_id).devices_models[device_id].test_type
    # 是否需要开启键盘向下的箭头(仅在解码时候出现)
    is_need_open_down: bool = False
    # 是否需要查询用户词数量
    is_need_user_words_count: bool = False
    # 创建参数对象
    parameter = Parameter(ime_type=ime_type,
                          ime_keyboard_type=keyboard_type,
                          output_type=output_type,
                          input_file_path=input_path_doc,
                          input_date_item_type=input_date_item_type,
                          is_need_match_step_decode=is_need_step_decoded,
                          is_need_check_net=is_need_check_net,
                          is_need_time_stamp=is_need_time_stamp,
                          is_pick_three_step_sys=is_three_steps_open,
                          is_need_user_word_count=is_need_user_words_count,
                          is_need_open=is_need_open_down)

    parameter.test_type = test_type

    if test_type == TestType.CloudLost:
        catch_cloud_action(parameter_inner=parameter)
    else:
        main(parameter_inner=parameter,
             device_index=device_id)


def run_async_task():
    """
    run the async task now
    :return:
    """
    if len(sys.argv) == 2:
        cu_device_index: int = int(sys.argv[1])
        old_ime_test(device_id=cu_device_index)
    else:
        print("System arguments error, should just give one parameter")


if __name__ == '__main__':
    run_async_task()
