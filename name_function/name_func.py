# coding: utf-8
# 人名模式测试
from Parameter import Parameter, ErrorInfoType, OutPutType, InputCom
from input import write_keyboard_input, enter_name_model_button, down_arrow_pressed
from socket_client import socket_input
from server import split_line_data, update_json, reset_result
from Model.ReturnTypeModel import ReturnTypeModel
from error.error_model import EmulatorError, InputError
from file_io import set_temp_file_info, writer
import time
from typing import Tuple, List

WAIT_NAME_MODEL_DELAY: int = 1


def name_func_test(inner_param: Parameter,
                   keyboard_input_str: str,
                   grape_word: str) -> Tuple[List[str], List[str], bool]:
    """
    人名模式测试
    :param inner_param: 输入模式
    :param keyboard_input_str: 输入键盘的单词
    :param grape_word: 选入的拼音
    :return: 返回人名模式前面的内容, 主词典解码
    """
    names: List[str] = []
    # 是不是两次点击才进入人名
    is_double_click: bool = False
    try:
        write_keyboard_input(word_code=keyboard_input_str,
                             keyboard_brand=inner_param.ime_type,
                             keyboard_type=inner_param.ime_keyboard_type)
        return_socket_str = socket_input(sock=inner_param.sock,
                                         sock_file=inner_param.sock_file)
        time.sleep(WAIT_NAME_MODEL_DELAY)
        can_in_name_mode, model = can_trigger_name_mode(result_json_str=return_socket_str,
                                                        inner_param=inner_param)
        main_dict = model.candidate_list
        if can_in_name_mode:
            # 进行人名模式解码
            names = decode_name_decodes(inner_param=inner_param)
        else:
            # 尝试再次点击下拉获取结果
            down_arrow_pressed(inner_param.simulator_process_id,
                               inputType=InputCom.Sogou)
            time.sleep(WAIT_NAME_MODEL_DELAY)
            # 再进行一次数据判断，能不能进入人名
            return_socket_str = socket_input(sock=inner_param.sock,
                                             sock_file=inner_param.sock_file)
            can_in_name_mode, model = can_trigger_name_mode(result_json_str=return_socket_str,
                                                            inner_param=inner_param)
            if can_in_name_mode:
                # 进行人名模式解码
                is_double_click = True
                names = decode_name_decodes(inner_param=inner_param)
        while model.candidate_length == 0:
            # 如果没有返回值就重启socket
            raise EmulatorError(message="解码结果没有候选词")

    except EmulatorError as emulatorError:
        # 重置键盘
        reset_result(len([grape_word]), inner_param)
        raise emulatorError
    except Exception as e:
        print(e)
        raise EmulatorError(message="其他异常报错")
    return names, main_dict, is_double_click


def can_trigger_name_mode(result_json_str: str,
                          inner_param: Parameter) -> Tuple[bool, ReturnTypeModel]:
    """
    根据返回的json数据结构判断能不能进入人名模式
    :param result_json_str: 返回的解码JSON数据
    :param inner_param: 获取参数
    :return:
    """
    if result_json_str is not None:
        model: ReturnTypeModel = update_json(return_socket_str=result_json_str,
                                             ime_type=inner_param.ime_type)
        if len(model.cloud_list) > 0 and '人名' in model.cloud_list[0]:
            return True, model
        else:
            return False, model
    else:
        return False, None


def decode_name_decodes(inner_param: Parameter) -> List[str]:
    """
    对人名模式进行解码
    :return: 返回人名模式解码数组
    """
    names: List[str] = []
    # 如果能进入人名进行解析
    enter_name_model_button(parameter=inner_param)
    print('进入人名模式')
    # 再次获取数据
    name_json_str = socket_input(sock=inner_param.sock,
                                 sock_file=inner_param.sock_file)
    if name_json_str is not None:
        name_model: ReturnTypeModel = update_json(return_socket_str=name_json_str,
                                                  ime_type=inner_param.ime_type)
        print('人名模式解码结果')
        names = name_model.candidate_list
        # 尝试再次点击下拉获取结果
        down_arrow_pressed(inner_param.simulator_process_id,
                           inputType=InputCom.Sogou)
        time.sleep(WAIT_NAME_MODEL_DELAY)
        # 尝试再次点击下拉获取结果
        down_arrow_pressed(inner_param.simulator_process_id,
                           inputType=InputCom.Sogou)
        time.sleep(WAIT_NAME_MODEL_DELAY)
    return names


def run_name_service(parameter: Parameter):
    """
    每次执行一个文件（即30w数据）
    :param parameter: 输入模式和参数
    :return:
    """
    # 从前一次位置继续执行抓取
    index = parameter.speed_of_progress["index"]
    new_current_file_date = parameter.file_data[index:]
    # 执行socket查询，并重置输入   line_data 类型为 json 或 str
    for line_data in new_current_file_date:
        index = index + 1
        # 获取 抓取py、抓取结果、上下文py、上下文结果
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
            # 人名模式的解码结果
            names, main_dict, is_double_click = name_func_test(inner_param=parameter,
                                                               sound_item_ascii_array=grasp_py_ascii_array,
                                                               grape_word=item_obj.grape_word)
            # 重置候选词和上屏结果
            reset_result(len(item_obj.grape_word), parameter)
            # 写入文件里面
            write_info_file(names=names,
                            pre_decode=item_obj.grape_word,
                            input_parameter=parameter,
                            index=index,
                            pre_name=item_obj.above_word,
                            candidates=main_dict,
                            is_double_click=is_double_click)
        except EmulatorError as emulatorError:
            raise emulatorError


def write_info_file(names: List[str],
                    candidates: List[str],
                    pre_decode: str,
                    pre_name: str,
                    input_parameter: Parameter,
                    is_double_click: bool,
                    index: int):
    """
    写入文件
    :param names: 人名数组
    :param input_parameter: 输入模式Model
    :param candidates: 主词典里面的解码
    :param index: 当前的索引
    :param pre_name: 预期人名
    :param is_double_click: 是不是两次进入人名模式
    :param pre_decode: 解码明文
    :return:
    """
    input_parameter.speed_of_progress["index"] = index  # 当前进度
    set_temp_file_info(input_parameter.speed_of_progress)
    # 获取本地
    if OutPutType.Local in input_parameter.output_type:
        line_str = f"#INPUT:{pre_decode};#PREDICT:{pre_name};#CANDIDATES:{candidates}"
        if len(names) > 0:
            line_str += f"#NAMES:{names}"
            if is_double_click:
                line_str += f"#DOUBLECLICK"
        else:
            line_str += f"#ERROR:没有进入人名模式"
        print(line_str)
        writer(file_name=input_parameter.speed_of_progress["client_file"],
               data=line_str,
               out_put_type=input_parameter.input_date_item_type)
