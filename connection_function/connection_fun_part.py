# coding: utf-8
# 上下文模式模块
# @Author  : haozhang45@iflytek.com
# @File    : main.py

from Model.InputItemObj import DoubleCommitModel
from error.error_model import EmulatorError
from file_io import *
from upper_screen import *
import json
from Parameter import *
from Model.OutputJsonModel import OutputJsonModel
from Model.ResultReturnModel import ResultReturnModel
from Model.ReturnTypeModel import ReturnTypeModel, DecodeReturnModel
from utils import create_time_stamp
from Model.ConnectionWriteModel import WriteConnectionModel


def split_connection_text_data(line_data: str, parameter: Parameter) -> [DoubleCommitModel]:
    """
    上下文属性下的字段分隔
    :param line_data: 读取测试集的每一行
    :param parameter: 模式的对象
    :return: 返回上下文属性的结果
    """
    items: [DoubleCommitModel] = []
    if parameter.input_date_item_type == FileReadType.Line:
        line_data = line_data.replace(' ', '').replace('\n', '').strip()
        line_data_array = line_data.split('|||')

        for index, item in enumerate(line_data_array):
            item_obj: DoubleCommitModel = DoubleCommitModel(above_word="",
                                                            grape_word="")
            item_array = item.split("#")
            item_obj.grape_word = item_array[0]
            if len(item_array) > 1:
                item_obj.above_word = item_array[1]
            items.append(item_obj)
    return items


def pick_word(candidate_list: [str],
              above_word: str,
              parameter_inner: Parameter,
              index: int,
              device_index: int) -> ErrorInfoType:
    """
    进行选词
    :param candidate_list: 候选词列表
    :param above_word: 上屏词汇
    :param parameter_inner: 输入番薯
    :param index: 选中的索引
    :param device_index: the index of devices
    :return: 返回是否成功
    """
    errorType: ErrorInfoType = ErrorInfoType.Success
    if above_word in candidate_list:
        # 如果有上屏结果，获取结果索引，并触发上屏，且重置候选词
        index = candidate_list.index(above_word)
        if index != -1:
            # 执行上屏. 搜狗的上屏操作
            send_upper_screen_request(parameter_inner.sock,
                                      parameter_inner.sock_file,
                                      index,
                                      True)
            time.sleep(IME_Constant.IME_COMMIT_DELAY_TIME)
            if parameter_inner.is_not_iflytek():
                # 搜狗需要按键触发
                enter_blank_space(parameter=parameter_inner,
                                  ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)

    else:
        # 没有完整的匹配结果，需要分段上屏
        result: ErrorInfoType = match_upper_screen(input_parameter=parameter_inner,
                                                   full_word="",
                                                   index=index,
                                                   candi_list=candidate_list,
                                                   above_result=above_word,
                                                   pick_step_num=0,
                                                   is_in_single_picker=False,
                                                   device_index=device_index)
        if result == ErrorInfoType.DecodeError or result == ErrorInfoType.OverflowStep:
            errorType = result
    return errorType


def run(parameter: Parameter,
        grape_word: str,
        above_word: str,
        is_not_commit: bool,
        device_index: int) -> DecodeReturnModel:
    """
    根据条件进行选词或者获取候选词
    :param parameter: 输入模式的参数
    :param grape_word:  获取候选词
    :param above_word: 需要上屏的词
    :param is_not_commit:  是否需要选词
    :param device_index: the index of devices
    :return: 返回候选的json数据Model
    """
    # 解码结果和联想结果初始化
    decode_return_model: DecodeReturnModel = DecodeReturnModel(
        associate_list=[],
        candidate_list=[],
        cloud_list=[],
        origin_json_str="",
        error_type=ErrorInfoType.Success,
        target_pos=0,
        net_work_status=True,
        time_stamp="",
        is_name_pattern=False,
        last_word=""
    )
    index = -1
    try:
        compose_target_word(sock=parameter.sock,
                            sock_file=parameter.sock_file,
                            target_word=above_word)
        write_keyboard_input(word_code=grape_word,
                             keyboard_type=parameter.ime_keyboard_type,
                             keyboard_brand=parameter.ime_type,
                             appium_utils=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
        return_socket_str = socket_input(sock=parameter.sock,
                                         sock_file=parameter.sock_file)
        # 获取时间戳
        time_stamp: str = create_time_stamp()
        if return_socket_str is not None:
            model: ReturnTypeModel = update_json(return_socket_str=return_socket_str,
                                                 ime_type=parameter.ime_type)
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
            decode_return_model.is_name_pattern = model.is_name_pattern
            while model.candidate_length == 0:
                # 如果没有返回值就重启socket
                raise EmulatorError(message="解码结果没有候选词")

            if not is_not_commit:
                # 进行选词功能
                result: ErrorInfoType = pick_word(candidate_list=decode_return_model.candidate_list,
                                                  index=index,
                                                  above_word=above_word,
                                                  parameter_inner=parameter,
                                                  device_index=device_index)
                decode_return_model.error_type = result

    except EmulatorError as emulatorError:
        # 重置键盘
        reset_result(word_len=len([grape_word]),
                     parameter=parameter,
                     device_index=device_index)
        raise emulatorError
    except Exception as e:
        print(e)
        raise EmulatorError(message="其他异常报错")
    return decode_return_model


def reset_result(word_len: int,
                 parameter: Parameter,
                 device_index: int):
    reset_input(parameter.sock, parameter.sock_file)
    if parameter.is_not_iflytek():
        if not parameter.is_need_user_word_count:
            delete_upper_screen_result(word_len=word_len,
                                       keyboard_brand=parameter.ime_type,
                                       keyboard_type=parameter.ime_keyboard_type,
                                       appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
        else:
            clear_button_action(parameter=parameter,
                                ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)


def run_connection_service(parameter: Parameter,
                           device_index: int):
    """
    每次执行一个文件（即30w数据）
    :param parameter: 输入模式和参数
    :param device_index: the index of device
    :return:
    """
    # 获取每一步上一次获取的候选词结果, 如果一致就是报错了
    previous_candidates: [str] = []
    previous_pinyin: str = ""
    # 用于记录总数
    # total_count = len(parameter.file_data)
    # 从前一次位置继续执行抓取
    index = parameter.speed_of_progress["index"]
    new_current_file_date = parameter.file_data[index:]
    # 执行socket查询，并重置输入   line_data 类型为 json 或 str
    for line_data in new_current_file_date:
        index = index + 1
        # 获取 抓取py、抓取结果、上下文py、上下文结果
        items: [DoubleCommitModel] = split_connection_text_data(line_data=line_data,
                                                                parameter=parameter)
        # 解码结果列表
        decode_list: [WriteConnectionModel] = []
        try:
            for select_index, select_word in enumerate(items):
                model: DecodeReturnModel = run(parameter=parameter,
                                               grape_word=select_word.grape_word,
                                               above_word=select_word.above_word,
                                               is_not_commit=(select_index == (len(items) - 1)),
                                               device_index=device_index)
                # 比较两次候选词是否一致，如果一致就报错(注意上屏的拼音也要不一致)
                if model.candidate_list == previous_candidates and \
                        select_word.grape_word != previous_pinyin and \
                        len(previous_pinyin) != 0:
                    raise EmulatorError(message="两次候选词结果一致，说明模拟器异常")
                # 重置每一次选词有可能的错误
                previous_candidates = model.candidate_list
                previous_pinyin = select_word.grape_word
                write_model: WriteConnectionModel = WriteConnectionModel(
                    candidate_list=model.candidate_list,
                    cloud_list=model.cloud_list,
                    above_word=select_word.above_word,
                    grape_word=select_word.grape_word,
                    origin_json_str=model.origin_json_str,
                    error_type=model.error_type,
                    previous_word="",
                    last_word=model.last_word
                )
                decode_list.append(write_model)
                if model.error_type != ErrorInfoType.Success:
                    # 一次发生错误就退出
                    break
            write_info_file(items=decode_list,
                            input_parameter=parameter,
                            index=index,
                            device_index=device_index)
            # 重置候选词和上屏结果
            reset_result(word_len=len(items[-1].grape_word),
                         parameter=parameter,
                         device_index=device_index)
            clear_button_action(parameter=parameter,
                                ba_appium_util=DeviceUtilsModel.shared(index=device_index).devices_appium_ms)
        except EmulatorError as emulatorError:
            raise emulatorError


def write_info_file(items: List[WriteConnectionModel],
                    input_parameter: Parameter,
                    index: int,
                    device_index: int):
    """
    写入文件
    :param items: 解码数组
    :param input_parameter: 输入模式Model
    :param index: 当前的索引
    :param device_index: the index of devices
    :return:
    """
    if len(items) == 0:
        return
    input_parameter.speed_of_progress["index"] = index  # 当前进度
    set_temp_file_info(device_index=device_index,
                       current_dict=input_parameter.speed_of_progress)
    origin_json_str: str = ""
    line_str: str = ""
    # 获取本地
    if OutPutType.Local in input_parameter.output_type:
        for write_item in items:
            origin_json_str += json.dumps(write_item.origin_json_str)
            line_str += write_item.model_to_json()
            line_str += '|||'
            if write_item.error_type != ErrorInfoType.Success:
                line_str += write_item.model_to_json()
        print(line_str)
        writer_full(input_parameter.speed_of_progress["client_file"], origin_json_str)
        writer(file_name=input_parameter.speed_of_progress["client_file"],
               data=line_str,
               out_put_type=input_parameter.input_date_item_type,
               device_index=device_index)


def update_json(return_socket_str: str,
                ime_type: InputCom) -> ReturnTypeModel:
    """
    获取socket返回json中候选词长度，并处理特殊格式 转化成统一格式
    :param return_socket_str: 获取的json字符串
    :param ime_type: 输入类型格式: 搜狗还是讯飞输入法
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
    if ime_type == InputCom.IflyTek or ime_type == InputCom.IflytekReal:
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
    return return_model
