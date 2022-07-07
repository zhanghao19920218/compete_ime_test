# coding=utf-8
# @author: haozhang45
# @date: 2022/2/12
# @description: 封装获取元素的方法
import time
from typing import List

from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from Parameter import InputCom
from appium_section.ba_adb import BAADB
from appium_section.keyboard_pos import KeyboardName
from appium_section.appium_driver import AppiumDriver
from appium_section.models.config_reader import DeviceModel
from error.error_model import AppiumError


class BAElement(object):
    """
    封装appium中关于元素对象的方法
    """
    _driver: WebDriver = None
    _at: AppiumDriver = None

    @property
    def get_driver(self) -> WebDriver:
        """
        Property for getting driver
        :return:
        """
        return self._driver

    @property
    def get_appium_driver(self) -> AppiumDriver:
        """
        return self define Appium Driver
        :return:
        """
        return self._at

    def quit_session(self):
        """
        quit the session part
        :return:
        """
        self._at.quit_session()

    def __init__(self,
                 model: DeviceModel):
        """
        initialization of webdriver and create by config.yaml
        :param model:
        """
        self._at = AppiumDriver(model=model)
        self._driver = self._at.get_driver()

    def start_app(self):
        """
        启动app
        :return:
        """
        self._at.run_app()

    def get_id(self, element_id: str) -> WebElement:
        """
        根据id获取元素
        :param element_id:
        :return:
        """
        try:
            element: WebElement = self._driver.find_element(by=By.ID, value=element_id)
            return element
        except AttributeError as attributeError:
            raise AppiumError(message=attributeError.args[0])
        except Exception as e:
            raise AppiumError(message="Appium Get Id Error!!!")

    def get_text(self, text: str) -> WebElement:
        """
        根据上面的字符串获取元素
        :param text:
        :return:

        """
        element: WebElement = self._driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                                        value=f'new UiSelector().text("{text}")')
        return element

    def get_element_by_scroll(self,
                              text: str) -> WebElement:
        """
        根据元素，通过滚动方式查找
        :param text:
        :return:
        """
        is_found = self.check_is_show_element(text=text)
        while not is_found:
            self._driver.swipe(
                start_x=int(self.get_screen_width / 2),
                start_y=int(self.get_screen_height / 4 * 3),
                end_x=int(self.get_screen_width / 2),
                end_y=int(self.get_screen_height / 2),
                duration=100
            )
            is_found = self.check_is_show_element(text=text)
        element: WebElement = self._driver.find_element(by=By.XPATH,
                                                        value=f'//*[@text="{text}"]/../../android.widget.LinearLayout/android.widget.CheckBox')
        return element

    def check_is_show_element(self,
                              text: str) -> bool:
        """
        查看是否找到该元素
        :param text:
        :return:
        """
        try:
            self._driver.implicitly_wait(5)
            self._driver.find_element(by=By.XPATH,
                                      value=f'//*[@text="{text}"]')
            return True
        except Exception as e:
            return False

    def get_text_check_box(self, text: str) -> WebElement:
        """
        根据text获取对应的checkbox
        :param text:
        :return:
        """
        element: WebElement = self._driver.find_element(by=By.XPATH,
                                                        value=f'//*[@text="{text}"]/../../android.widget.LinearLayout/android.widget.CheckBox')
        return element

    def send_event(self,
                   key_event: int = 84):
        """
        输入法输入键盘
        :param key_event:
        :return:
        """
        self._driver.keyevent(keycode=key_event)

    def driver_wait(self, seconds: int):
        self._driver.implicitly_wait(seconds)

    def click_keyboard(self,
                       key_board_name: KeyboardName):
        """
        点击键盘
        :param key_board_name: 键盘类型
        :return:
        """
        try:
            action = TouchAction(self._driver)
            action.tap(x=key_board_name.x,
                       y=key_board_name.y).perform()
        except AttributeError as attributeError:
            raise AppiumError(message=attributeError.args[0])
        except Exception:
            raise AppiumError(message="Touch Action others Error!!!")

    def scroll_keyboard(self,
                        start_pos: KeyboardName,
                        end_pos: KeyboardName):
        """
        滑动键盘
        :param start_pos:
        :param end_pos:
        :return:
        """
        self._driver.swipe(
            start_x=start_pos.x,
            start_y=start_pos.y,
            end_x=end_pos.x,
            end_y=end_pos.y,
            duration=500
        )

    def long_press_keyboard(self,
                            key_board_name: KeyboardName,
                            duration_time: int):
        """
        长按键盘
        :param key_board_name: 键盘类型
        :param duration_time: 长按键盘
        :return:
        """
        try:
            action = TouchAction(self._driver)
            action.long_press(x=key_board_name.x,
                              y=key_board_name.y,
                              duration=duration_time).perform()
        except AttributeError as attributeError:
            raise AppiumError(message=attributeError.args[0])
        except Exception:
            raise AppiumError(message="Touch Action others Error!!!")

    def set_ime_keyboard(self,
                         keyboard_brand: InputCom):
        """
        设置输入法
        :param keyboard_brand: 输入法的brand
        :return:
        """
        self._driver.activate_ime_engine(engine=BAADB.get_package_name(apk_type=keyboard_brand))

    def hide_ime_keyboard(self):
        """
        隐藏键盘
        :return:
        """
        self._driver.hide_keyboard()

    def is_show_keyboard(self) -> bool:
        """
        是否收起键盘
        :return:
        """
        return self._driver.is_keyboard_shown()

    def go_back(self):
        """
        Go back to the main screen
        :return:
        """
        self._driver.back()

    @property
    def get_screen_width(self) -> int:
        """
        获取屏幕宽度
        :return:
        """
        return self._at.get_screen_width

    @property
    def get_screen_height(self) -> int:
        """
        获取屏幕高度
        :return:
        """
        return self._at.get_screen_height
