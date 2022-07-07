# coding=utf-8
# @author: haozhang45
# @date: 2022/2/28
# @description: 测试demo
import os
import time

from Model.device_utils_model import DeviceUtilsModel
from Parameter import KeyboardType
from baappiumutils import BAAppiumUtils
from Parameter import InputCom
from appium_section.models.config_reader import ConfigReader
from utils import run_multiprocess


def run_demo(device_index: int,
             device_type: InputCom):
    config_reader: ConfigReader = ConfigReader.from_yaml(yaml_file="../config/config.yaml")
    common_driver: BAAppiumUtils = DeviceUtilsModel.shared().devices_appium_ms[device_index]
    common_driver.set_ime_keyboard(ime_type=device_type)
    time.sleep(5)
    common_driver.get_input_text_view()
    # common_driver.get_input_text_view()
    time.sleep(2)
    port: str = DeviceUtilsModel.shared().devices_models[device_index].connectPort
    # os.system(f'adb -s {DeviceUtilsModel.shared().devices_models[device_index].deviceName} forward tcp:{port} tcp:' + port)
    common_driver.change_menu(key_board_brand=InputCom.IflytekReal,
                              key_board_type=KeyboardType.Keyboard26Key,
                              is_english=False)
    for alpha_tmp in 'abcdefghijklmnopqrstuvwxyz':
        # common_driver.input_alpha_26key(key_board_brand=InputCom.IflytekReal,
        #                                 alpha_letter=alpha_tmp)
        common_driver.input_alpha_26key(key_board_brand=InputCom.IflytekReal,
                                        alpha_letter=alpha_tmp)
    common_driver.quit_session()


if __name__ == '__main__':
    print("测试完成")
    device_model = DeviceUtilsModel.shared(index=0).devices_models[0]
    common_driver: BAAppiumUtils = DeviceUtilsModel.shared(index=0).devices_appium_ms
    # common_driver.set_ime_keyboard(ime_type=device_model.keyboard_type)
    # time.sleep(2)
    common_driver.wait_seconds(2)
    common_driver.get_input_text_view()
    common_driver.get_input_text_view()
    # time.sleep(0.5)
    common_driver.change_menu(key_board_type=KeyboardType.Keyboard26Key,
                              key_board_brand=InputCom.IflytekReal,
                              is_english=False)
    for alpha_tmp in 'zuotiannichilema':
        common_driver.input_alpha_26key(key_board_brand=InputCom.IflytekReal,
                                        alpha_letter=alpha_tmp)
    common_driver.down_arrow_action(key_board_brand=InputCom.IflytekReal)
    common_driver.press_single_pick(key_board_brand=InputCom.IflytekReal)
    common_driver.choose_more_candidates(keyboard_brand=InputCom.IflytekReal)
    common_driver.press_single_pick(key_board_brand=InputCom.IflytekReal)
    common_driver.choose_more_candidates(keyboard_brand=InputCom.IflytekReal)
    common_driver.delete_more_candidates(keyboard_brand=InputCom.IflytekReal)
    common_driver.choose_more_candidates(keyboard_brand=InputCom.IflytekReal)
    # devices_id = [0, 1]
    # device_models = DeviceUtilsModel.shared(index=devices_id).devices_appium_ms
    # devices_type = [InputCom.IflyTek, InputCom.IflytekReal]
    # params = [
    #     {
    #         "index": 0,
    #         "type": devices_type[0]
    #     },
    #     {
    #         "index": 1,
    #         "type": devices_type[1]
    #     }
    # ]
    # run_multiprocess(func=run_demo,
    #                  parameters=params)
