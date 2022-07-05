#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : haozhang45@iflytek.com
# @Updated : haozhang45@iflytek.com
# @Time    : 2019-09-17 10:46
# @File    : upper_screen.py
from typing import List
from input import *
from socket_client import *
from Parameter import InputCom, ErrorInfoType
from Model.ReturnTypeModel import ReturnTypeModel
from Model.OutputJsonModel import OutputJsonModel
from Model.ResultReturnModel import ResultReturnModel


def above_update_json(return_socket_str: str,
                      ime_type: InputCom) -> ReturnTypeModel:
    """
    上屏候选词解码
    :param return_socket_str: 返回的json数据字符串
    :param ime_type: 输入法类型:讯飞还是搜狗
    :return:
    """
    return_model: ReturnTypeModel = ReturnTypeModel(
        cloud_list=[],
        candidate_list=[],
        candidate_length=0,
        origin_json="",
        target_pos=0,
        last_word="",
        is_name_pattern=False
    )
    return_socket_json = json.loads(return_socket_str)
    cloud_result_list: List[str] = []  # 云端结果数组
    if ime_type == InputCom.IflyTek:
        model = ResultReturnModel.dict_to_object(return_socket_json)
        # 判断是否有运算结果
        cloud_result: str = model.result.result.result.candidates.cloud
        if cloud_result is not None:
            cloud_result_list.append(cloud_result)
        force_cloud_result: str = model.result.result.result.candidates.force_cloud
        if force_cloud_result is not None:
            cloud_result_list.append(force_cloud_result)
        return_model.cloud_list = cloud_result_list
        return_model.candidate_list = model.result.result.result.candidates.candidates_list
        return_model.candidate_length = len(return_model.candidate_list)
        return_model.origin_json = model.result.origin_json
    else:
        model: OutputJsonModel = OutputJsonModel.dict_to_object(return_socket_json)
        # 判断是否有运算结果
        cloud_result: str = model.result.cloud
        if len(cloud_result.strip()) != 0 and cloud_result is not None:
            cloud_result_list.append(cloud_result)
        return_model.cloud_list = cloud_result_list
        return_model.candidate_list = model.result.candidates
        return_model.candidate_length = len(return_model.candidate_list)
        return_model.origin_json = return_socket_json
        return_model.last_word = model.result.last_word
    return return_model


def match_upper_screen(input_parameter: Parameter,
                       full_word: str,
                       index: int,
                       candi_list: List[str],
                       above_result: str,
                       pick_step_num: int,
                       is_in_single_picker: bool,
                       device_index: int) -> ErrorInfoType:
    """
    分步选词
    :param input_parameter: 输入模式参数
    :param full_word: 整个词语
    :param index: 分步选词的index
    :param candi_list: 候选列表
    :param above_result: 上屏结果
    :param pick_step_num: 分步选词的步数，如果大于1
    :param is_in_single_picker: 是不是要进行单字选词
    :param device_index: the index of device
    :return: 错误类型
    """
    if index == -1:
        # 如果单字选词就跳转单字选词
        if is_in_single_picker:
            single_word_pick_result(ime_type=input_parameter.ime_type,
                                    appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
            # 获取上屏后的候选词列表
            return_socket_str: str = socket_input(input_parameter.sock, input_parameter.sock_file)
            if return_socket_str is not None:
                model: ReturnTypeModel = above_update_json(return_socket_str, input_parameter.ime_type)
                candi_list = model.candidate_list  # 更新最新的候选列表
                for item in model.candidate_list:
                    if item in above_result[len(full_word):len(full_word) + len(item)]:
                        index = candi_list.index(item)
                        full_word = full_word + item
                        break
                if index == -1:
                    # 单字选词也没有改词汇，选择报错
                    if input_parameter.ime_type == InputCom.Baidu:
                        back_line_candidate(ime_type=input_parameter.ime_type,
                                            appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
                    errorType = ErrorInfoType.DecodeError
                    return errorType  # 返回报错信息
                else:
                    return match_upper_screen(
                        input_parameter=input_parameter,
                        full_word=full_word,
                        index=index,
                        candi_list=candi_list,
                        above_result=above_result,
                        pick_step_num=pick_step_num,
                        is_in_single_picker=is_in_single_picker,
                        device_index=device_index
                    )
            else:
                # 单字选词也没有改词汇，选择报错
                if input_parameter.ime_type == InputCom.Baidu:
                    back_line_candidate(ime_type=input_parameter.ime_type,
                                        appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
                errorType = ErrorInfoType.DecodeError
                return errorType

        else:
            for item in candi_list:
                if item in above_result[len(full_word):len(full_word) + len(item)]:
                    index = candi_list.index(item)
                    full_word = full_word + item
                    break
            # 是否需要单字选词
            is_single_pick: bool = index == -1
            return match_upper_screen(
                input_parameter=input_parameter,
                full_word=full_word,
                index=index,
                candi_list=candi_list,
                above_result=above_result,
                pick_step_num=pick_step_num,
                is_in_single_picker=is_single_pick,
                device_index=device_index
            )
    else:
        pick_step_num += 1
        # 如果分步选词的步数大于3，就相当于获取联想失效
        if pick_step_num > 3 and input_parameter.is_pick_three_step_sys:
            # 如果打开了候选词界面，需要关闭候选词
            if is_in_single_picker and input_parameter.ime_type == InputCom.Baidu:
                back_line_candidate(ime_type=input_parameter.ime_type,
                                    appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
            errorType = ErrorInfoType.OverflowStep
            return errorType
        else:
            send_upper_screen_request(input_parameter.sock, input_parameter.sock_file, index, False)
            time.sleep(IME_Constant.IME_COMMIT_DELAY_TIME)
            if input_parameter.is_not_iflytek():
                # 搜狗需要按键触发
                enter_blank_space(parameter=input_parameter,
                                  ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
            # 如果打开了候选词界面，需要关闭候选词
            if is_in_single_picker:
                # 重新关闭单字选词
                is_in_single_picker = False
                if input_parameter.ime_type == InputCom.IflyTek:
                    # 如果是讯飞输入法, 关闭候选词界面
                    down_arrow_pressed(ime_type=input_parameter.ime_type,
                                       appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
                elif input_parameter.ime_type == InputCom.Baidu and full_word != above_result:
                    back_line_candidate(ime_type=input_parameter.ime_type,
                                        appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)

            # 获取上屏后的候选词列表
            return_socket_str = socket_input(input_parameter.sock, input_parameter.sock_file)
            if return_socket_str is not None:
                json_model: ReturnTypeModel = above_update_json(return_socket_str=return_socket_str,
                                                                ime_type=input_parameter.ime_type)
                candi_list = json_model.candidate_list
                if full_word != above_result:
                    return match_upper_screen(input_parameter=input_parameter,
                                              full_word=full_word,
                                              index=-1,
                                              candi_list=candi_list,
                                              above_result=above_result,
                                              is_in_single_picker=is_in_single_picker,
                                              pick_step_num=pick_step_num,
                                              device_index=device_index)
                else:
                    # 选词成功
                    errorType = ErrorInfoType.Success
                    return errorType
            else:
                if input_parameter.ime_type == InputCom.Baidu:
                    back_line_candidate(ime_type=input_parameter.ime_type,
                                        appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
                errorType = ErrorInfoType.DecodeError
                return errorType
