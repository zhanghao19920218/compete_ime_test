# coding=utf-8
# @author: haozhang45
# @date: 2022/2/12
# @description: 封装appium的driver模块, 目前仅测试Mumu模拟器，所以用的是127.0.0.1:62001
# @updateDate: 2022/05/13
# @updateDescription: 修改为真机测试，从MetaSingleton改为普通object类
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from error.error_model import AppiumErrorType, AppiumError
from appium_section.ba_adb import BAADB
from appium_section.models.config_reader import DeviceModel


class AppiumDriver(object):
    driver: WebDriver = None
    _screen_width: int = 0
    _screen_height: int = 0

    def __init__(self,
                 model: DeviceModel):
        """
        According to Device Model to create Appium WebDriver
        :param model: Device Model from `config.yaml` File
        """
        if self.driver is None:
            desired_caps: dict = {"platformName": model.platformName,
                                  "platformVersion": model.platformVersion,
                                  "deviceName": model.deviceName,
                                  "appPackage": model.appPackage,
                                  "appActivity": model.appActivity,
                                  "newCommandTimeout": int(model.newCommandTimeout),
                                  "automationName": "UiAutomator2",
                                  "systemPort": f"{model.systemPort}",
                                  "udid": model.udid,
                                  'noReset': model.noReset}
            # GIve chance ten times to create driver
            for i in range(10):
                try:
                    connect_url: str = f"http://localhost:{model.port}/wd/hub"
                    print(connect_url)
                    self.create_driver(command_executor=f"http://localhost:{model.port}/wd/hub",
                                       desired_capabilities=desired_caps)
                    break
                except AppiumError as appium_error:
                    print(appium_error.get_error_type.value)
            if self.driver is not None:
                self.driver.implicitly_wait(time_to_wait=30)

            # Get the screen height, width not from appium. because it's not suitable for screen
            ba_adb: BAADB = BAADB(device_name=model.deviceName)
            self._screen_width = ba_adb.get_screen_size().width
            self._screen_height = ba_adb.get_screen_size().height

    def create_driver(self,
                      command_executor: str,
                      desired_capabilities: dict):
        """
        Static method create Appium Driver
        :param command_executor:
        :param desired_capabilities:
        :return:
        """
        try:
            self.driver = webdriver.Remote(command_executor=command_executor,
                                           desired_capabilities=desired_capabilities)
        except Exception as e:
            print(e)
            raise AppiumError(error_type=AppiumErrorType.DRIVER_ERROR)

    def get_driver(self) -> WebDriver:
        """
        Get the driver of Appium webdriver. if none return throw Exception
        :return:
        """
        if self.driver is None:
            raise AppiumError(error_type=AppiumErrorType.NO_DEVICE_CONNECT)
        return self.driver

    def run_app(self):
        """
        启动app
        :return:
        """
        self.driver.launch_app()

    def quit_session(self):
        """
        Close the session
        :return:
        """
        self.driver.quit()

    @property
    def get_screen_width(self) -> int:
        """
        返回屏幕宽度
        :return:
        """
        return self._screen_width

    @property
    def get_screen_height(self) -> int:
        """
        返回屏幕高度
        :return:
        """
        return self._screen_height
