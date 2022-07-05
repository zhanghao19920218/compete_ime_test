# coding: utf-8
# 测试云端数据丢失接口文档
from time import struct_time

from Model.InputItemObj import InputItemObj
from error.error_model import EmulatorError
from file_io import *
from upper_screen import *
import json
import urllib.request
from Parameter import *
from Model.OutputJsonModel import OutputJsonModel
from Model.ResultReturnModel import ResultReturnModel
from Model.ReturnTypeModel import ReturnTypeModel, DecodeReturnModel
from utils import create_time_stamp

# 云端请求间隔
CLOUD_SLEEP_TIME: int = 2


def net_work_status_check() -> bool:
    """查询当前的网络状态"""
    try:
        urllib.request.urlopen('http://baidu.com')  # Python 3.x
        return True
    except:
        return False


def run(parameter: Parameter,
        py_str: str,
        is_check_net: bool) -> DecodeReturnModel:
    """
    根据条件进行选词或者获取候选词
    :param parameter: 输入模式的参数
    :param py_str:  获取候选词
    :param is_check_net: 是否需要检测网络
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
        time_stamp=""
    )
    try:
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
            while model.candidate_length == 0:
                # 如果没有返回值就重启socket
                raise EmulatorError(message="解码结果没有候选词")
    except EmulatorError as emulatorError:
        # 重置键盘
        reset_result(len([py_str]), parameter)
        raise emulatorError
    except Exception as e:
        print(e)
        raise EmulatorError(message="其他异常报错")
    return decode_return_model


def reset_result(word_len, parameter):
    reset_input(parameter.sock, parameter.sock_file)
    delete_upper_screen_result(parameter=parameter,
                               word_len=word_len + 1)


def run_service_cloud(parameter: Parameter):
    """
    每次执行一个文件（即30w数据）
    :param parameter: 输入模式和参数
    :return:
    """
    # 用于记录总数
    # total_count = len(parameter.file_data)
    # 从前一次位置继续执行抓取
    index: int = 0
    # 获取模拟器聚焦
    get_window_rect()
    # 获取 抓取py、抓取结果、上下文py、上下文结果
    item_obj: InputItemObj = InputItemObj(
        above_word='怪女人',
        associate_word='',
        grape_word='guainvren',
        is_need_commit=False
    )

    # 获取py对应的ascii码数组
    grasp_py_ascii_array = format_line(keyboard_type=parameter.ime_keyboard_type,
                                       line=item_obj.grape_word)
    # 输入全部字符
    write_keyboard_input(grasp_py_ascii_array,
                         parameter,
                         is_need_commit=False)
    # 执行socket查询，并重置输入   line_data 类型为 json 或 str
    while index != 30000:
        index = index + 1
        # 回删一次，再输入一次
        remove_one_char(parameter=parameter)
        # 输入一个字符
        write_keyboard_last_char(grasp_py_ascii_array[-1],
                                 parameter)
        # 请求云端结果
        time.sleep(CLOUD_SLEEP_TIME)
        # 进行候选或者上屏操作
        try:
            model: DecodeReturnModel = run(parameter=parameter,
                                           py_str=item_obj.grape_word,
                                           is_check_net=(index % 5 == 0))

            write_info_file(candidate_list=model.candidate_list,
                            pre_decode=item_obj.grape_word,
                            input_parameter=parameter,
                            cloud_list=model.cloud_list,
                            index=index,
                            target_pos=model.target_pos,
                            error_type=model.error_type,
                            net_work_status=model.net_work_status,
                            origin_json_str=model.origin_json_str,
                            time_stamp=model.time_stamp)
        except EmulatorError as emulatorError:
            raise emulatorError


def write_info_file(candidate_list: List[str],
                    cloud_list: List[str],
                    pre_decode: str,
                    origin_json_str: str,
                    input_parameter: Parameter,
                    error_type: ErrorInfoType,
                    net_work_status: bool,
                    target_pos: int,
                    time_stamp: str,
                    index: int):
    """
    写入文件
    :param candidate_list: 解码数组
    :param cloud_list: 云端解码数组
    :param input_parameter: 输入模式Model
    :param index: 当前的索引
    :param origin_json_str: 原始的json字符串, 方便后面写入log
    :param error_type: 错误类型
    :param pre_decode: 解码明文
    :param target_pos: 目标位置
    :param net_work_status: 网络接连是否正常
    :param time_stamp: 当前时间戳
    :return:
    """
    if len(candidate_list) == 0:
        return
    # 获取本地
    if OutPutType.Local in input_parameter.output_type:
        line_str = f"#INPUT:{pre_decode};#CLOUD_WORDS:{cloud_list}"
        if error_type != ErrorInfoType.Success:
            line_str = f"#INPUT:{pre_decode};#ERROR:{'解码错误' if error_type == ErrorInfoType.DecodeError else '超出选词步数'}"
        if input_parameter.is_need_match_step_decode:
            line_str += f"#GET_LOCATION:{target_pos}"
        if not net_work_status:
            line_str += f"#NETWORK:CONNECT ERROR"
        if input_parameter.is_need_time_stamp:
            line_str += f"#TIMESTAMP:{time_stamp};#TIME:{time_stamp_convert(time_num=time_stamp)}"
        print(line_str)
        write_cloud(file_name=IME_Constant.CLOUD_LOST_FILE,
                    data=line_str)


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
        target_pos=0
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
        return_model.target_pos = model.result.target
    return return_model


def time_stamp_convert(time_num: str) -> str:
    """
    时间戳转换
    :param time_num: 毫秒时间戳
    :return: 时间格式字符串
    """
    # 毫秒转化为秒
    time_stamp: float = float(int(time_num) / 1000)
    # 获取时间数组
    time_array: struct_time = time.localtime(time_stamp)
    # 转化为时间
    time_stamp_str: str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return time_stamp_str
