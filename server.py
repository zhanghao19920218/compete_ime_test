#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : haozhang45@iflytek.com
# @Time    : 2019-03-11 11:34
# @File    : server.py
# @UpdateBy: HaoZhang45
import time

from Model.InputItemObj import InputItemObj
from Model.encode_json_model import EncodeJsonModel
from error.error_model import EmulatorError, InputError, AppiumError
from file_io import *
from upper_screen import *
import json
import urllib.request
from Parameter import *
from Model.OutputJsonModel import OutputJsonModel
from Model.ResultReturnModel import ResultReturnModel
from Model.ReturnTypeModel import ReturnTypeModel, DecodeReturnModel
from utils import create_time_stamp, pinyin_to_num


def net_work_status_check() -> bool:
    """查询当前的网络状态"""
    try:
        urllib.request.urlopen('http://baidu.com')  # Python 3.x
        return True
    except:
        return False


# 9443#资格#789426#取消
def split_line_data(line_data: str, parameter: Parameter) -> InputItemObj:
    """
    读取文件每一行进行数据分隔
    :param line_data: 读取测试集的每一行
    :param parameter: 模式的对象
    :return:
    """
    item_obj: InputItemObj = InputItemObj(above_word="", grape_word="", associate_word="", is_need_commit=False)
    if parameter.input_date_item_type == FileReadType.Line:
        line_data = line_data.replace(' ', '').replace('\n', '').strip()
        line_data_array = line_data.split('|||')

        for item in line_data_array:
            if IME_Constant.IME_NEED_COMMIT_STR in item:
                item_obj.is_need_commit = True
                item_array = item.split(IME_Constant.IME_NEED_COMMIT_STR)
                item_obj.associate_word = item_array[1]
                item_grape_array = item_array[0].split("#")
                item_obj.grape_word = item_grape_array[0]
                if len(item_grape_array) > 1:
                    item_obj.above_word = item_grape_array[1]
            else:
                item_array = item.split("#")
                input_keys: str = item_array[0]  # 获取输入的键盘
                if len(input_keys) == 0: raise InputError(message="输入的长度为0",
                                                          value=10)
                item_obj.grape_word = item_array[0]
                if len(item_array) > 1:
                    item_obj.above_word = item_array[1]
    return item_obj


# @with_goto
def run(parameter: Parameter,
        complete_word: str,
        py_str: str,
        above_word: str,
        is_check_net: bool,
        is_upper: bool,
        device_index: int) -> DecodeReturnModel:
    """
    根据条件进行选词或者获取候选词
    :param parameter: 输入模式的参数
    :param complete_word: 完整的词汇
    :param py_str:  获取候选词
    :param above_word: 需要上屏的词
    :param is_upper: 是否需要上屏
    :param is_check_net: 是否需要检测网络
    :param device_index: 设备的index
    :return: 返回候选的json数据Model
    """
    # 解码结果和联想结果初始化
    # label.begin
    decode_return_model: DecodeReturnModel = DecodeReturnModel(
        associate_list=[],
        candidate_list=[],
        cloud_list=[],
        origin_json_str="",
        error_type=ErrorInfoType.Success,
        target_pos=0,
        net_work_status=True,
        time_stamp="",
        last_word="",
        is_name_pattern=False,
        pinyin=""
    )
    index = -1
    try:
        # 先选词composing
        if parameter.is_need_match_step_decode:
            compose_target_word(sock=parameter.sock,
                                sock_file=parameter.sock_file,
                                target_word=above_word)
        # 按键输入
        keyboard_input_words(input_parameter=parameter,
                             complete_word=complete_word,
                             is_upper=is_upper,
                             py_str=py_str,
                             device_index=device_index)
        # 需要等待云端结果
        time.sleep(0.5)
        # 是否需要展开(仅在解码是否可以强制加入)
        if not is_upper and parameter.is_need_open:
            down_arrow_pressed(ime_type=parameter.ime_type,
                               appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
        # 检查网络状态是否正常
        if is_check_net and parameter.is_need_check_network:
            print("检测网络")
            decode_return_model.net_work_status = net_work_status_check()
        return_socket_str = socket_input(sock=parameter.sock,
                                         sock_file=parameter.sock_file)
        # 获取时间戳
        time_stamp: str = create_time_stamp()
        if return_socket_str is not None:
            model: ReturnTypeModel = update_json(return_socket_str=return_socket_str,
                                                 ime_type=parameter.ime_type,
                                                 is_nine=parameter.ime_keyboard_type == KeyboardType.Keyboard9Key)
            # 获取解码结果
            decode_return_model.candidate_list = model.candidate_list
            # 获取云端解码结果
            decode_return_model.cloud_list = model.cloud_list
            # 获取原始解码数据
            decode_return_model.origin_json_str = model.origin_json
            # 获取当前解码的位置
            decode_return_model.target_pos = model.target_pos
            # 获取当前时间戳
            decode_return_model.time_stamp = time_stamp
            # 返回显屏词
            decode_return_model.last_word = model.last_word
            decode_return_model.pinyin = model.pinyin
            decode_return_model.is_name_pattern = model.is_name_pattern
            while model.candidate_length == 0:
                # 如果没有返回值就重启socket
                raise EmulatorError(message="解码结果没有候选词")
            pinyin_tmp: str = pinyin_to_num(pinyin=complete_word) if parameter.ime_keyboard_type == KeyboardType.Keyboard9Key else complete_word
            if pinyin_tmp != decode_return_model.pinyin and not parameter.is_not_iflytek():
                raise EmulatorError(message="拼音字符串不一致")
            # 云端解码结果没出
            # while len(model.cloud_list) == 0 and IME_Constant.IME_REBOOT_SOCKET_TIMES > 0:
            #     # 重置键盘
            #     reset_result(len([py_str]), parameter)
            #     print(IME_Constant.IME_REBOOT_SOCKET_TIMES)
            #     IME_Constant.IME_REBOOT_SOCKET_TIMES = IME_Constant.IME_REBOOT_SOCKET_TIMES - 1
            #     # 如果没有云端结果就返回第一行重新执行
            #     goto .begin
            if is_upper:
                if above_word in decode_return_model.candidate_list:
                    # 如果有上屏结果，获取结果索引，并触发上屏，且重置候选词
                    index = model.candidate_list.index(above_word)
                    if index != -1:
                        # 执行上屏. 搜狗的上屏操作
                        send_upper_screen_request(parameter.sock, parameter.sock_file, index, True)
                        time.sleep(IME_Constant.IME_COMMIT_DELAY_TIME)
                        if parameter.is_not_iflytek():
                            # 搜狗需要按键触发
                            enter_blank_space(parameter=parameter,
                                              ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
                        # 上屏之后获取候选词(也就是所谓的联想词汇)
                        associate_json_str: str = socket_associate(sock=parameter.sock,
                                                                   sock_file=parameter.sock_file)

                        if associate_json_str is not None:
                            decode_return_model.error_type = ErrorInfoType.Success
                            associate_model: ReturnTypeModel = update_json(return_socket_str=associate_json_str,
                                                                           ime_type=parameter.ime_type,
                                                                           is_nine=parameter.ime_keyboard_type == KeyboardType.Keyboard9Key)
                            decode_return_model.associate_list = associate_model.candidate_list
                            if associate_model.candidate_list == model.candidate_list:
                                raise EmulatorError(message="解码结果和联想结果一致，没有触发点击键")

                else:
                    # 没有完整的匹配结果，需要分段上屏
                    result: ErrorInfoType = match_upper_screen(input_parameter=parameter,
                                                               full_word="",
                                                               index=index,
                                                               candi_list=model.candidate_list,
                                                               above_result=above_word,
                                                               pick_step_num=0,
                                                               is_in_single_picker=False,
                                                               device_index=device_index)
                    if result == ErrorInfoType.DecodeError or result == ErrorInfoType.OverflowStep:
                        decode_return_model.error_type = result
                    else:
                        # 上屏之后获取候选词(也就是所谓的联想词汇)
                        associate_json_str: str = socket_associate(sock=parameter.sock,
                                                                   sock_file=parameter.sock_file)
                        if associate_json_str is not None:
                            decode_return_model.error_type = ErrorInfoType.Success
                            associate_model: ReturnTypeModel = update_json(return_socket_str=associate_json_str,
                                                                           ime_type=parameter.ime_type,
                                                                           is_nine=parameter.ime_keyboard_type == KeyboardType.Keyboard9Key)
                            decode_return_model.associate_list = associate_model.candidate_list
    except EmulatorError as emulatorError:
        # 重置键盘
        reset_result(len([py_str]),
                     parameter,
                     device_index)
        raise emulatorError
    except AppiumError as appiumError:
        # 如果是Appium问题, 关闭键盘
        hide_keyboard(ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
        raise appiumError
    except Exception as e:
        print(e)
        raise EmulatorError(message="其他异常报错")
    return decode_return_model


def reset_result(word_len, parameter, device_index):
    reset_input(parameter.sock, parameter.sock_file)
    if parameter.ime_type == InputCom.Baidu:
        if not parameter.is_need_user_word_count:
            delete_upper_screen_result(word_len=word_len,
                                       keyboard_brand=parameter.ime_type,
                                       keyboard_type=parameter.ime_keyboard_type,
                                       appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
    clear_button_action(parameter=parameter,
                        ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)


def run_service(parameter: Parameter,
                device_index: int):
    """
    每次执行一个文件（即30w数据）
    :param parameter: 输入模式和参数
    :param device_index: 设备index
    :return:
    """
    # 获取每一步上一次获取的候选词结果, 如果一致就是报错了
    previous_candidates: List[str] = []
    previous_pinyin: str = ""
    # 从前一次位置继续执行抓取
    index = parameter.speed_of_progress["index"]
    new_current_file_date = parameter.file_data[index:]
    # 执行socket查询，并重置输入   line_data 类型为 json 或 str
    for line_data in new_current_file_date:
        index = index + 1
        # 获取 抓取py、抓取结果、上下文py、上下文结果
        try:
            item_obj = split_line_data(line_data=line_data,
                                       parameter=parameter)
        except InputError as inputError:
            if inputError.value == 10:
                # 显示这是一个错误的输入值
                print(inputError.message)
                continue
        # 进行候选或者上屏操作
        try:
            model: DecodeReturnModel = run(parameter=parameter,
                                           complete_word=item_obj.grape_word,
                                           py_str=item_obj.grape_word,
                                           above_word=item_obj.above_word,
                                           is_upper=item_obj.is_need_commit,
                                           is_check_net=(index % 5 == 0),
                                           device_index=device_index)
            # 比较两次候选词是否一致，如果一致就报错(注意上屏的拼音也要不一致)
            if model.candidate_list == previous_candidates and \
                    item_obj.grape_word != previous_pinyin and \
                    len(previous_pinyin) != 0:
                raise EmulatorError(message="两次候选词结果一致，说明模拟器异常")

            # 获取用户词数量
            if parameter.is_need_user_word_count:
                pressed_enter(keyboard_brand=parameter.ime_type,
                              ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
                # catch_user_words_dict(sock=parameter.sock,
                #                       sock_file=parameter.sock_file)
                # ret: str = get_user_word_count(sock=parameter.sock,
                #                                sock_file=parameter.sock_file)
                # print(ret)

            write_info_file(candidate_list=model.candidate_list,
                            pre_decode=item_obj.grape_word,
                            expect_word=item_obj.above_word,
                            associate_list=model.associate_list,
                            expect_associate=item_obj.associate_word,
                            input_parameter=parameter,
                            cloud_list=model.cloud_list,
                            index=index,
                            target_pos=model.target_pos,
                            error_type=model.error_type,
                            net_work_status=model.net_work_status,
                            origin_json_str=model.origin_json_str,
                            last_word=model.last_word,
                            time_stamp=model.time_stamp,
                            is_name_pattern=model.is_name_pattern,
                            device_index=device_index)
            # 重置没有云端结果次数
            IME_Constant.IME_REBOOT_SOCKET_TIMES = 2
            previous_candidates = model.candidate_list
            previous_pinyin = item_obj.grape_word
            # 重置候选词和上屏结果
            if item_obj.is_need_commit:
                reset_result(word_len=len(item_obj.above_word),
                             parameter=parameter,
                             device_index=device_index)
            reset_result(word_len=len(item_obj.grape_word),
                         parameter=parameter,
                         device_index=device_index)
        except EmulatorError as emulatorError:
            raise emulatorError
        except AppiumError as appiumError:
            raise appiumError


def write_info_file(candidate_list: List[str],
                    cloud_list: List[str],
                    pre_decode: str,
                    expect_word: str,
                    associate_list: List[str],
                    expect_associate: str,
                    origin_json_str: str,
                    input_parameter: Parameter,
                    error_type: ErrorInfoType,
                    net_work_status: bool,
                    last_word: str,
                    target_pos: int,
                    time_stamp: str,
                    device_index: int,
                    is_name_pattern: bool,
                    index: int):
    """
    写入文件
    :param candidate_list: 解码数组
    :param associate_list: 联想数组
    :param cloud_list: 云端解码数组
    :param input_parameter: 输入模式Model
    :param index: 当前的索引
    :param expect_associate: 期望联想
    :param expect_word: 期望选词
    :param origin_json_str: 原始的json字符串, 方便后面写入log
    :param error_type: 错误类型
    :param pre_decode: 解码明文
    :param target_pos: 目标位置
    :param net_work_status: 网络接连是否正常
    :param time_stamp: 当前时间戳
    :param last_word: 屏显最后一位的词
    :param is_name_pattern: 是否开启人名模式
    :param device_index: 设备里面的index
    :return:
    """
    if len(candidate_list) == 0:
        return
    input_parameter.speed_of_progress["index"] = index  # 当前进度
    set_temp_file_info(current_dict=input_parameter.speed_of_progress,
                       device_index=device_index)
    # 获取本地
    if OutPutType.Local in input_parameter.output_type:
        encode_model: EncodeJsonModel = EncodeJsonModel()
        encode_model.input_keys = pre_decode
        encode_model.expect_word = expect_word
        encode_model.candidates = candidate_list
        encode_model.expect_associate = expect_associate
        encode_model.associate_candi = associate_list
        encode_model.cloud_candi = cloud_list
        encode_model.error_type = error_type
        encode_model.is_calculate = input_parameter.is_need_match_step_decode
        encode_model.input_num = target_pos
        encode_model.is_net_connect = not net_work_status
        encode_model.is_need_time_stamp = input_parameter.is_need_time_stamp
        encode_model.time_stamp = time_stamp
        encode_model.last_word = last_word
        encode_model.is_name_pattern = is_name_pattern
        line_str: str = encode_model.model_to_json()
        # 拼接设备名和文件名
        file_name: str = input_parameter.speed_of_progress["client_file"].replace(".txt", f"_{DeviceUtilsModel.shared(index=device_index).devices_models[device_index].deviceName.replace(':', '_').replace('.', '_')}.txt")
        print(line_str)
        writer_full(file_name=file_name,
                    json_data=origin_json_str)
        writer(file_name=file_name,
               data=line_str,
               out_put_type=input_parameter.input_date_item_type,
               device_index=device_index)


def update_json(return_socket_str: str,
                ime_type: InputCom,
                is_nine: bool) -> ReturnTypeModel:
    """
    获取socket返回json中候选词长度，并处理特殊格式 转化成统一格式
    :param return_socket_str: 获取的json字符串
    :param ime_type: 输入类型格式: 搜狗还是讯飞输入法
    :param is_nine: 是否是9key
    :return:
    """
    return_model: ReturnTypeModel = ReturnTypeModel(
        cloud_list=[],
        candidate_list=[],
        candidate_length=0,
        origin_json="",
        target_pos=0,
        last_word="",
        is_name_pattern=False,
        pinyin=""
    )
    return_socket_json = json.loads(return_socket_str)
    cloud_result_list: List[str] = []  # 云端结果数组
    if ime_type == InputCom.IflyTek or ime_type == InputCom.IflytekReal:
        model:ResultReturnModel = ResultReturnModel.dict_to_object(return_socket_json)
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
        return_model.target_pos = model.result.result.result.candidates.target
        return_model.is_name_pattern = model.result.result.result.is_name_pattern
        return_model.last_word = model.result.result.result.last_word
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
        return_model.target_pos = model.result.target
        return_model.last_word = model.result.last_word
        return_model.pinyin = model.result.pinyin if not is_nine else pinyin_to_num(pinyin=model.result.pinyin)
    return return_model


def keyboard_input_words(input_parameter: Parameter,
                         complete_word: str,
                         is_upper: bool,
                         device_index: int,
                         py_str: str):
    """
    键盘输入
    :param input_parameter:
    :param complete_word: 上屏词
    :param is_upper: 是否上屏，上屏就不点击后面一个键
    :param device_index: 选中设备的index
    :param py_str: 拼音位数
    :return:
    """
    write_keyboard_input(word_code=complete_word,
                         keyboard_type=input_parameter.ime_keyboard_type,
                         keyboard_brand=input_parameter.ime_type,
                         appium_utils=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
    # 选词最后一位, 但是不上屏, 需要反hook一下
    if not is_upper and not input_parameter.is_need_open and not input_parameter.ime_type == InputCom.IflyTek:
        compose_last_word(sock=input_parameter.sock,
                          sock_file=input_parameter.sock_file)
        press_last_word_pos(keyboard_brand=input_parameter.ime_type,
                            ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
    # if input_parameter.ime_type == InputCom.Baidu and not is_upper:
    #     reset_result(word_len=len(py_str),
    #                  parameter=input_parameter,
    #                  device_index=device_index)
    #     write_keyboard_input(word_code=complete_word,
    #                          keyboard_type=input_parameter.ime_keyboard_type,
    #                          keyboard_brand=input_parameter.ime_type,
    #                          appium_utils=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
