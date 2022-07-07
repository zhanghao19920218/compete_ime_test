# coding=utf-8
# @author: haozhang45
# @date: 2022/2/12
# @description: 获取一些通用方法
import time
from appium.webdriver import WebElement
from Parameter import KeyboardType, InputCom
from appium_section.ba_element import BAElement
from appium_section.keyboard_pos import KeyboardPos
from appium_section.models.config_reader import DeviceModel


class BAAppiumUtils(object):
    """
    封装一些通用方法
    """

    def __init__(self,
                 model: DeviceModel):
        self.el: BAElement = BAElement(model=model)

    def start_app(self):
        """
        启动app
        :return:
        """
        self.el.start_app()

    def quit_session(self):
        """
        Close the session
        :return:
        """
        self.el.quit_session()

    def wait_seconds(self, seconds: int):
        """
        wait for some seconds
        :param seconds:
        :return:
        """
        self.el.driver_wait(seconds=seconds)

    def back_action(self):
        """
        back to parent page
        :return:
        """
        self.el.get_driver.back()

    def get_input_text_view(self):
        """
        获取text_view然后进行聚焦
        :return:
        """
        self.el.get_id(element_id="com.iflytek.inputmethod.imehook:id/editText").click()

    def choose_word(self,
                    key_board_brand: InputCom):
        """
        选词按键
        :param key_board_brand: 按键品牌名称
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .Choose_Word())

    def delete_action(self,
                      key_board_brand: InputCom,
                      key_board_type: KeyboardType,
                      duration_time: int):
        """
        选词按键
        :param key_board_brand: 按键品牌名称
        :param key_board_type: 键盘类型: 26键或者9键
        :param duration_time: 按键延迟时间
        :return:
        """
        self.el.long_press_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                               screen_height=self.el.get_screen_height)
                                    .Delete_Action(keyboard_ime=key_board_type),
                                    duration_time=duration_time)

    def write_input_text(self,
                         word: str):
        """
        输入法输入字符串
        :param word:
        :return:
        """
        self.el.get_id(element_id="com.iflytek.inputmethod.imehook:id/editText").send_keys(word)

    def change_menu(self,
                    key_board_brand: InputCom,
                    key_board_type: KeyboardType,
                    is_english: bool):
        """
        根据键盘类型修改键盘
        :param key_board_type:
        :param key_board_brand: 键盘品牌
        :param is_english: 是否是英文输入
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .MenuKeyBoard())
        # time.sleep(0.5)
        if is_english:
            if key_board_type == KeyboardType.Keyboard9Key:
                self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                                  screen_height=self.el.get_screen_height)
                                       .NineEn())
            else:
                self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                                  screen_height=self.el.get_screen_height)
                                       .SixEn())
        else:
            if key_board_type == KeyboardType.Keyboard9Key:
                self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                                  screen_height=self.el.get_screen_height)
                                       .NineCh())
            else:
                self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                                  screen_height=self.el.get_screen_height)
                                       .SixCh())

    def menu_setting(self,
                     key_board_brand: InputCom):
        """
        键盘详情设置
        :param key_board_brand:
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .DetailSetting())
        time.sleep(1)
        for i in range(2):
            self.el.scroll_keyboard(
                start_pos=KeyboardPos(keyboard_type=key_board_brand,
                                      screen_height=self.el.get_screen_height).PageBelowPos(
                    screen_height=self.el.get_screen_height,
                    screen_width=self.el.get_screen_width
                ),
                end_pos=KeyboardPos(keyboard_type=key_board_brand,
                                    screen_height=self.el.get_screen_height).PageTopPos(
                    screen_width=self.el.get_screen_width
                )
            )
            time.sleep(0.5)
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .MoreSetting(
            screen_height=self.el.get_screen_height
        ))

    def check_is_fuzzy(self,
                       set_fuzzy: bool = True):
        """
        查看是否是纠错音
        :return:
        """
        self.el.get_text(text="输入设置").click()
        self.el.get_driver.implicitly_wait(2)
        # check fuzzy mode is switched on, if not, shut down
        fuzzy_check_box: WebElement = self.el.get_element_by_scroll(text="误按键纠错")
        if set_fuzzy:
            if fuzzy_check_box.get_attribute(name="checked") != 'true':
                fuzzy_check_box.click()
        else:
            if fuzzy_check_box.get_attribute(name="checked") == 'true':
                fuzzy_check_box.click()

    def input_alpha_26key(self,
                          key_board_brand: InputCom,
                          alpha_letter: str):
        """
        输入键盘的字母
        :param key_board_brand: 键盘品牌
        :param alpha_letter: 阿拉伯字母
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .AlphaKeyName(alpha_name=alpha_letter))

    def input_alpha_9key(self,
                         key_board_brand: InputCom,
                         alpha_letter: str):
        """
        输入键盘的字母
        :param key_board_brand: 键盘品牌
        :param alpha_letter: 阿拉伯字母
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .NumLetter(alpha_name=alpha_letter))

    def write_string(self,
                     key_board_brand: InputCom,
                     keyboard_type: KeyboardType,
                     word: str):
        """
        根据str写入word
        :param word:
        :param keyboard_type: 键盘类型
        :param key_board_brand: 输入法的品牌
        :return:
        """
        for alpha_tmp in word:
            if keyboard_type == KeyboardType.Keyboard26Key:
                self.input_alpha_26key(key_board_brand=key_board_brand,
                                       alpha_letter=alpha_tmp)
            else:
                self.input_alpha_9key(key_board_brand=key_board_brand,
                                      alpha_letter=alpha_tmp)
            time.sleep(0.2)

    def down_arrow_action(self,
                          key_board_brand: InputCom):
        """
        点击下拉显示更多按钮
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .DownArrow_Action())

    def back_line_action(self,
                         key_board_brand: InputCom):
        """
        返回显示更多界面
        :param key_board_brand:
        :return:
        """
        self.el.go_back()
        # self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
        #                                                   screen_height=self.el.get_screen_height)
        #                        .Keyboard_Return())

    def clear_button_action(self,
                            key_board_brand: InputCom):
        """
        点击清除内容的按钮
        :return:
        """
        self.el.get_id(element_id="com.iflytek.inputmethod.imehook:id/button").click()

    def press_last_word(self,
                        key_board_brand: InputCom):
        """
        点击选词最后一位
        :param key_board_brand: 键盘品牌
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .Keyboard_Last_Word())

    def press_baidu_next_page(self):
        """
        点击百度输入法下一个页面的按钮
        :return: 返回百度输入法的下一个页面的按钮位置
        """
        self.el.click_keyboard(key_board_name=KeyboardPos.Keyboard_Baidu_NextPage())

    def set_ime_keyboard(self,
                         ime_type: InputCom):
        """
        切换输入法类型
        :param ime_type: 输入法类型
        :return:
        """
        self.el.set_ime_keyboard(keyboard_brand=ime_type)

    def hide_keyboard(self):
        """
        收起键盘
        :return:
        """
        self.el.hide_ime_keyboard()

    def is_show_keyboard(self) -> bool:
        """
        是否显示键盘
        :return:
        """
        return self.el.is_show_keyboard()

    def pressed_enter_button(self,
                             key_board_brand: InputCom):
        """
        点击输入按钮
        :param key_board_brand:
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .Keyboard_Enter())

    def press_single_pick(self,
                          key_board_brand: InputCom):
        """
        pressed single and word switch
        :param key_board_brand:
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=key_board_brand,
                                                          screen_height=self.el.get_screen_height)
                               .Keyboard_SwitchSingle())

    def choose_more_candidates(self,
                               keyboard_brand: InputCom):
        """
        pressed single and word
        :param keyboard_brand:
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=keyboard_brand,
                                                          screen_height=self.el.get_screen_height)
                               .Keyboard_More_ChooseWord())

    def delete_more_candidates(self,
                               keyboard_brand: InputCom):
        """
        delete more candidates
        :param keyboard_brand:
        :return:
        """
        self.el.click_keyboard(key_board_name=KeyboardPos(keyboard_type=keyboard_brand,
                                                          screen_height=self.el.get_screen_height)
                               .KeyBoard_More_Delete())

