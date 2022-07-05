# coding=utf-8
# Get the model from configuration
from typing import List
from yaml import safe_load

from Parameter import InputCom, KeyboardType, TestType


class DeviceModel(object):
    """
    设备的model
    """
    platformName: str = ""

    platformVersion: str = ""

    deviceName: str = ""

    appPackage: str = ""

    appActivity: str = ""

    newCommandTimeout: str = ""

    noReset: bool = False

    port: str = ""

    systemPort: str = ""

    udid: str = ""

    iflytekPort: str = ""

    ime_type: InputCom = InputCom.IflyTek

    # Read the test case file path
    read_file_path: str = ""

    keyboard_type: KeyboardType = KeyboardType.Keyboard26Key

    test_type: TestType = TestType.Decode

    def __init__(self,
                 platformName: str,
                 platformVersion: str,
                 appPackage: str,
                 deviceName: str,
                 appActivity: str,
                 newCommandTimeout: str,
                 port: str,
                 noReset: bool,
                 systemPort: str,
                 iflytekPort: str,
                 ime_type: InputCom,
                 read_file_path: str,
                 keyboard_type: KeyboardType,
                 test_type: TestType):
        """
        初始化设备
        :param platformName:
        :param platformVersion:
        :param appPackage:
        :param deviceName:
        :param appActivity:
        :param newCommandTimeout:
        :param port: Appium端口号
        :param noReset:
        :param systemPort: 系统端口
        :param iflytekPort: 讯飞输入法的端口号
        :param connectPort: 接口端口号
        :param ime_type: 输入法的类型
        :param read_file_path: read the test cases from directory
        :param keyboard_type: keyboard 26key or 9key
        :param test_type: the type of test
        """
        self.platformName = platformName
        self.platformVersion = platformVersion
        self.appPackage = appPackage
        self.appActivity = appActivity
        self.newCommandTimeout = newCommandTimeout
        self.noReset = noReset
        self.deviceName = deviceName
        self.port = port
        self.systemPort = systemPort
        self.udid = deviceName
        self.iflytekPort = iflytekPort
        self.ime_type = ime_type
        self.read_file_path = read_file_path
        self.keyboard_type = keyboard_type
        self.test_type = test_type

    @staticmethod
    def yaml_to_model(dict_info: dict):
        """
        解析yaml里面文件为model
        :param dict_info: 字典内容
        :return:
        """
        return DeviceModel(
            platformName=dict_info["platformName"],
            platformVersion=dict_info["platformVersion"],
            appPackage=dict_info["appPackage"],
            appActivity=dict_info["appActivity"],
            newCommandTimeout=dict_info["newCommandTimeout"],
            noReset=dict_info["noReset"],
            deviceName=dict_info["deviceName"],
            port=dict_info["port"],
            systemPort=dict_info['systemPort'],
            iflytekPort=dict_info['iflytekPort'],
            ime_type=InputCom(dict_info['brand']),
            read_file_path=dict_info['read_file_path'],
            keyboard_type=KeyboardType(dict_info['keyboard_type']),
            test_type=TestType(dict_info['test_type'])
        )


class ConfigReader(object):
    """
    Read models from configuration
    """
    devices: List[DeviceModel] = []

    def __init__(self,
                 devices: List[DeviceModel]):
        self.devices = devices

    @staticmethod
    def from_yaml(yaml_file: str):
        """
        读取yaml文件
        :param yaml_file:
        :return:
        """
        with open(file=yaml_file,
                  mode='rt',
                  encoding='utf-8') as yaml_file:
            yaml_dict: dict = safe_load(yaml_file)
            yaml_list: List[dict] = yaml_dict["test_devices"]
            devices: List[DeviceModel] = list(map(lambda item: DeviceModel.yaml_to_model(dict_info=item), yaml_list))
            return ConfigReader(
                devices=devices
            )


if __name__ == '__main__':
    config_model: ConfigReader = ConfigReader.from_yaml(yaml_file="../../config/config.yaml")
    print(config_model.devices[0].deviceName)
    if config_model.devices[0].noReset:
        print("Fuck")
