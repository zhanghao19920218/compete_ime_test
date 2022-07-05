# coding=utf-8
"""
@File    : device_utils_model.py
@Time    : 2022/6/13 15:26
@Author  : haozhang45
@Email   : haozhang45@iflytek.com
@Software : PyCharm
@Description: 设备的单例Model
"""
import time
from typing import List

from appium_section.baappiumutils import BAAppiumUtils
from constant import CONFIG_POS
from Model.singleton_meta import SingletonMeta
from appium_section.models.config_reader import DeviceModel, ConfigReader


class DeviceUtilsModel(metaclass=SingletonMeta):
    """
    设备的Model, 单例模式
    """
    devices_models: List[DeviceModel] = []

    devices_appium_ms: BAAppiumUtils = None

    select_index: int = 0

    def __init__(self):
        self.devices_models = []
        self.devices_appium_ms = None

    @staticmethod
    def shared(index: int):
        """

        :return:
        """
        device_model = DeviceUtilsModel()
        device_model.select_index = index
        if device_model.devices_appium_ms is None:
            device_model.config_devices()
        return device_model

    def config_devices(self):
        """
        设备配置
        :return:
        """
        config_reader: ConfigReader = ConfigReader.from_yaml(yaml_file=CONFIG_POS)
        self.devices_models = config_reader.devices
        for index, device_model in enumerate(config_reader.devices):
            if index == self.select_index:
                # 首先杀死设备进程
                print(f"当前端口号${device_model.deviceName}")
                # kill_port_process(ports=[f"{device_model.port}"])
                self.devices_appium_ms = BAAppiumUtils(model=device_model)
