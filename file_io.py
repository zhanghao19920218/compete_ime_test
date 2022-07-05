#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : haozhang45@iflytek.com
# @Time    : 2019-03-11 14:02
# @File    : file_io.py
# @Update  : Mason
import os
import json
from typing import List
from constant import INDEX_JSON_PATH
from Model.device_utils_model import DeviceUtilsModel
from Parameter import FileReadType
from engine_part.engine_mappy import EngineMethod, EngineMethodAction

writer_log_path = os.getcwd() + "/logs/"
writer_full_log_path = os.getcwd() + "/full_logs/"
check_error_correct_writer_path = os.getcwd() + "/checks/"
check_all_error_correct_writer_path = os.getcwd() + "/checks_all/"
cloud_logs_path = os.getcwd() + "/cloud_logs/"
index_info_path: str = os.path.abspath(os.path.join(os.getcwd(), INDEX_JSON_PATH))


def get_current_data(path: str,
                     read_type: FileReadType) -> list:
    return reader(path=path,
                  read_type=read_type)


def reader(path: str,
           read_type: FileReadType) -> List[str]:
    """
    读取纠错音文件
    :param path: 文件路径
    :param read_type: 读取文件方式
    :return:
    """
    with open(path, encoding='utf-8') as error_correct_file:
        error_correct_list = []
        line = error_correct_file.readline()  # 获取每一行数据
        if read_type == FileReadType.Line or read_type == FileReadType.SpecialLine:
            while line:
                error_correct_list.append(line)
                line = error_correct_file.readline()
        else:
            error_item = {}
            while line != "":
                error_item["input"] = line
                error_item["list"] = []
                error_item["list"].append(line)
                line = error_correct_file.readline()
                error_item["list"].append(line)
                line = error_correct_file.readline()
                error_item["list"].append(line)

                error_correct_list.append(error_item)
                error_item = {}
                line = error_correct_file.readline()
                if line.find("\n") > -1:
                    line = error_correct_file.readline()
        error_correct_file.close()
        return error_correct_list


# writer str / json
def writer(file_name: str,
           data: str,
           out_put_type: FileReadType,
           device_index: int):
    """
    写入Log文件
    :param file_name: 文件名称
    :param data: 文件行数
    :param out_put_type: 输出类型
    :param device_index: 设备的index
    :return:
    """
    device_name: str = DeviceUtilsModel.shared(index=device_index).devices_models[device_index].deviceName\
        .replace(".", "_").replace(":", "_")
    device_path: str = os.path.abspath(os.path.join(writer_log_path, device_name))
    if not os.path.exists(device_path):
        os.makedirs(device_path)
    with open(os.path.abspath(os.path.join(device_path,file_name)), 'a+', encoding='utf-8', errors='ignore') as error_correct_file:
        if out_put_type == FileReadType.Line:
            error_correct_file.write(data + "\n")
        elif out_put_type == FileReadType.SpecialLine:
            error_correct_file.write(data + "\n")
        else:
            for item in data:
                error_correct_file.write(item)
            error_correct_file.write("\n\n")


# writer str / json
def writer_full(file_name, json_data):
    with open(writer_full_log_path + file_name, 'a+', encoding='utf-8', errors='ignore') as error_correct_file:
        error_correct_file.write(str(json_data))
        error_correct_file.write("\n")
        error_correct_file.close()


# 写入云端结果
def write_cloud(file_name: str,
                data: str):
    """
    写入云端丢失效果
    :param file_name:
    :param data:
    :return:
    """
    with open(cloud_logs_path + file_name, 'a+', encoding='utf-8', errors='ignore') as error_correct_file:
        error_correct_file.write(data + "\n")
        error_correct_file.close()


def error_correct_read_gbk(path):
    with open(path, 'r', encoding='gb18030', errors='ignore') as error_correct_file:
        error_correct_list = []
        line = error_correct_file.readline()  # 调用文件的 readline()方法
        while line:
            error_correct_list.append(line)
            line = error_correct_file.readline()
        error_correct_file.close()
        return error_correct_list


def get_temp_file_info(device_index: int):
    """
    获取暂停抓取位置
    :param device_index: 设备配置里面的index
    :return: 获取抓取的index
    """
    ret: dict = {}
    device_name: str = DeviceUtilsModel.shared(index=device_index).devices_models[device_index].deviceName.replace(".", "_").replace(":", "_")
    index_path: str = os.path.join(index_info_path, f"{device_name}.json")
    if os.path.exists(index_path):
        with open(file=index_path,
                  mode='rt',
                  encoding='utf-8') as temp_info_file:
            ret = json.load(temp_info_file)
    return ret


# 写入被纠错音文件
def set_temp_file_info(device_index: int,
                       current_dict: dict):
    """
    设备id, 文件信息
    :param device_index: get index of devices
    :param current_dict: 当前设备的json数据
    :return:
    """
    device_name: str = DeviceUtilsModel.shared(index=device_index).devices_models[device_index].deviceName.replace(".", "_").replace(":", "_")
    if os.path.exists(index_info_path):
        index_path: str = os.path.join(index_info_path, f"{device_name}.json")
        with open(file=index_path,
                  mode='wt',
                  encoding='utf-8') as temp_info_file:
            json.dump(current_dict, temp_info_file, ensure_ascii=False, indent=4)


# 输入拼音抓取结果直接写入
def error_correct_writer(file_name, str):
    with open(writer_log_path + file_name, 'a+', encoding='gb18030', errors='ignore') as error_correct_file:
        error_correct_file.write(str + '\n')
        error_correct_file.close()


# 抓取结果 分析含有拼音即写入文件
def error_correct_writer_check(file_name, str):
    with open(check_error_correct_writer_path + file_name, 'a+', encoding='gb18030',
              errors='ignore') as error_correct_file:
        error_correct_file.write(str + '\n')
        error_correct_file.close()


# 抓取结果 分析含有拼音，并且必须文字结果一致写入
def error_all_correct_writer_check(file_name, str):
    with open(check_all_error_correct_writer_path + file_name, 'a+', encoding='gb18030',
              errors='ignore') as error_correct_file:
        error_correct_file.write(str + '\n')
        error_correct_file.close()


def read_engine_cases(engine_file: str) -> List[EngineMethodAction]:
    """
    读取引擎测试集获取测试解码
    :param engine_file: read the engine file
    :return:
    """
    action_list: List[EngineMethodAction] = []
    with open(file=engine_file,
              mode='rt',
              encoding='utf-8') as read_file:
        temp_lines: List[str] = read_file.readlines()
    for index, temp_line in enumerate(temp_lines):
        replace_temp_line: str = temp_line.strip()  # To strip the str
        if replace_temp_line.startswith("#"):
            # to get the tmp models of action
            tmp_model: EngineMethodAction = EngineMethodAction(method_name=EngineMethod(value=replace_temp_line),
                                                               method_action=temp_lines[
                                                                   index + 1].strip() if index < len(
                                                                   temp_lines) - 1 else "")
            action_list.append(tmp_model)
    return action_list
