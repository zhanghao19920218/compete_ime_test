# coding=utf-8
# @author: haozhang45
# @date: 2022/3/21
# @description:
import time

from Parameter import InputCom
from appium_section.models.config_reader import ConfigReader
from file_io import read_engine_cases
from typing import List
from engine_mappy import EngineMethodAction
from eng_case_model import EngineCaseModel

if __name__ == '__main__':
    # get device first
    config_reader: ConfigReader = ConfigReader.from_yaml(yaml_file="../config/config.yaml")
    action_list: List[EngineMethodAction] = read_engine_cases(engine_file="../testcases/CREATE_ASSOCIATE_001_SELECTWORD_26KEY_PY.TXT")
    model: EngineCaseModel = EngineCaseModel(keyboard_brand=InputCom.IflytekReal,
                                             device_model=config_reader.devices[0])
    # run action in single test case
    for action in action_list:
        time.sleep(0.5)
        # create random function

        model.engine_method_dict[action.method_name](action.method_action)
