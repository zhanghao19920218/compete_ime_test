# coding=utf-8
# @author: haozhang45
# @date: 2022/2/28
# @description: 搜狗输入法的按键
from Model.mobile_size_model import MobileSizeModel, ItemSizeModel, CoordinateModel
from Parameter import InputCom, KeyboardType


class KeyboardName(object):
    """
    获取键盘类型
    """
    x: int = 0  # x轴的位置

    y: int = 0  # y轴的位置

    def __init__(self,
                 x: int,
                 y: int):
        self.x = x
        self.y = y


class KeyboardPos(object):
    """
    键盘位置
    """

    keyboard_type: InputCom = InputCom.Sogou  # 输入法的类型
    keyboard_real_pos: MobileSizeModel = None
    single_item_size: ItemSizeModel = None
    single_item_9key_size: ItemSizeModel = None
    key26_q: CoordinateModel  # Keyboard 26keys Q Button Position
    key26_a: CoordinateModel  # Keyboard 26keys A Button Position
    key26_z: CoordinateModel  # Keyboard 26keys Z Button Position
    key9_smell: CoordinateModel  # Keyboard 9keys Smell Button Position

    def __init__(self,
                 keyboard_type: InputCom,
                 screen_height: int):
        self.keyboard_type = keyboard_type
        if self.keyboard_real_pos is None and keyboard_type == InputCom.IflytekReal:
            self.keyboard_real_pos = MobileSizeModel.json_to_object(screen_height=screen_height)
            self.single_item_size = self.keyboard_real_pos.wid_1080_model.keys_26key.single_item
            self.single_item_9key_size = self.keyboard_real_pos.wid_1080_model.keys_9key.single_item
            self.key26_q = self.keyboard_real_pos.wid_1080_model.keys_26key.keys_q
            self.key26_a = self.keyboard_real_pos.wid_1080_model.keys_26key.keys_a
            self.key26_z = self.keyboard_real_pos.wid_1080_model.keys_26key.keys_z

            self.key9_smell = self.keyboard_real_pos.wid_1080_model.keys_9key.keys_smell

            # 更新a的y轴
            self.key26_a.y = self.key26_q.y + self.single_item_size.height
            # 更新z的y轴
            self.key26_z.y = self.key26_q.y + (2 * self.single_item_size.height)

    def AlphaKeyName(self,
                     alpha_name: str) -> KeyboardName:
        """
        输入阿拉伯字符串
        :param alpha_name:
        :return:
        """
        if alpha_name == 'Q' or alpha_name == 'q':
            return self.Keyboard_Q()
        elif alpha_name == 'W' or alpha_name == 'w':
            return self.Keyboard_W()
        elif alpha_name == 'E' or alpha_name == 'e':
            return self.Keyboard_E()
        elif alpha_name == 'R' or alpha_name == 'r':
            return self.Keyboard_R()
        elif alpha_name == 'T' or alpha_name == 't':
            return self.Keyboard_T()
        elif alpha_name == 'Y' or alpha_name == 'y':
            return self.Keyboard_Y()
        elif alpha_name == 'U' or alpha_name == 'u':
            return self.Keyboard_U()
        elif alpha_name == 'I' or alpha_name == 'i':
            return self.Keyboard_I()
        elif alpha_name == 'O' or alpha_name == 'o':
            return self.Keyboard_O()
        elif alpha_name == 'P' or alpha_name == 'p':
            return self.Keyboard_P()
        elif alpha_name == 'A' or alpha_name == 'a':
            return self.Keyboard_A()
        elif alpha_name == 'S' or alpha_name == 's':
            return self.Keyboard_S()
        elif alpha_name == 'D' or alpha_name == 'd':
            return self.Keyboard_D()
        elif alpha_name == 'F' or alpha_name == 'f':
            return self.Keyboard_F()
        elif alpha_name == 'G' or alpha_name == 'g':
            return self.Keyboard_G()
        elif alpha_name == 'H' or alpha_name == 'h':
            return self.Keyboard_H()
        elif alpha_name == 'J' or alpha_name == 'j':
            return self.Keyboard_J()
        elif alpha_name == 'K' or alpha_name == 'k':
            return self.Keyboard_K()
        elif alpha_name == 'L' or alpha_name == 'l':
            return self.Keyboard_L()
        elif alpha_name == 'Z' or alpha_name == 'z':
            return self.Keyboard_Z()
        elif alpha_name == 'X' or alpha_name == 'x':
            return self.Keyboard_X()
        elif alpha_name == 'C' or alpha_name == 'c':
            return self.Keyboard_C()
        elif alpha_name == 'V' or alpha_name == 'v':
            return self.Keyboard_V()
        elif alpha_name == 'B' or alpha_name == 'b':
            return self.Keyboard_B()
        elif alpha_name == 'N' or alpha_name == 'n':
            return self.Keyboard_N()
        elif alpha_name == 'M' or alpha_name == 'm':
            return self.Keyboard_M()

    def NumLetter(self,
                  alpha_name: str):
        """
        输入9键的字母
        :param alpha_name:
        :return:
        """
        if alpha_name == '2' or alpha_name.lower() in 'abc':
            return self.Keyboard_ABC()
        elif alpha_name == '3' or alpha_name.lower() in 'def':
            return self.Keyboard_DEF()
        elif alpha_name == '4' or alpha_name.lower() in 'ghi':
            return self.Keyboard_GHI()
        elif alpha_name == '5' or alpha_name.lower() in 'jkl':
            return self.Keyboard_JKL()
        elif alpha_name == '6' or alpha_name.lower() in 'mno':
            return self.Keyboard_MNO()
        elif alpha_name == '7' or alpha_name.lower() in 'pqrs':
            return self.Keyboard_PQRS()
        elif alpha_name == '8' or alpha_name.lower() in 'tuv':
            return self.Keyboard_TUV()
        elif alpha_name == '9' or alpha_name.lower() in 'wxyz':
            return self.Keyboard_WXYZ()

    def MenuKeyBoard(self) -> KeyboardName:
        """
        切换键盘
        :return: 返回键盘类型
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=318, y=1005)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=325, y=1005)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.keyboard_real_pos.wid_1080_model.menu_key.x,
                                y=self.keyboard_real_pos.wid_1080_model.menu_key.y)
        else:
            return KeyboardName(x=223, y=960)

    def DetailSetting(self) -> KeyboardName:
        """
        键盘详细设置
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=72, y=1010)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=72, y=1010)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.keyboard_real_pos.wid_1080_model.setting_key.x,
                                y=self.keyboard_real_pos.wid_1080_model.menu_key.y)
        else:
            return KeyboardName(x=72, y=966)

    def PageBelowPos(self,
                     screen_height: float = 0,
                     screen_width: float = 0) -> KeyboardName:
        """
        界面底部的
        :param screen_height: 真机需要设备高度
        :param screen_width: 真机需要设备宽度
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=450, y=1580)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=450, y=1580)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=int(screen_width / 2),
                                y=self.keyboard_real_pos.wid_1080_model.keys_26key.keys_z.y)
        else:
            return KeyboardName(x=450, y=1580)

    def PageTopPos(self,
                   screen_width: float = 0) -> KeyboardName:
        """
        键盘最高的点
        :param screen_width: 滑动需要的设备宽度
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=450, y=1020)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=450, y=1020)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=int(screen_width / 2),
                                y=self.keyboard_real_pos.wid_1080_model.keys_26key.keys_q.y)
        else:
            return KeyboardName(x=450, y=1020)

    def MoreSetting(self,
                    screen_height: float = 0) -> KeyboardName:
        """
        更多设置
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=750, y=1245)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=750, y=1245)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.keyboard_real_pos.wid_1080_model.all_setting.x,
                                y=self.keyboard_real_pos.wid_1080_model.all_setting.y)
        else:
            return KeyboardName(x=750, y=1245)

    def NineCh(self) -> KeyboardName:
        """
        拼音九键
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=157, y=1100)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=120, y=1150)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.keyboard_real_pos.wid_1080_model.pinyin_9key.x,
                                y=self.keyboard_real_pos.wid_1080_model.pinyin_9key.y)
        else:
            return KeyboardName(x=120, y=1110)

    def SixCh(self) -> KeyboardName:
        """
        拼音全键
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=370, y=1100)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=342, y=1150)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.keyboard_real_pos.wid_1080_model.pinyin_26key.x,
                                y=self.keyboard_real_pos.wid_1080_model.pinyin_9key.y)
        else:
            return KeyboardName(x=350, y=1110)

    def NineEn(self) -> KeyboardName:
        """
        9键英文
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=768, y=1320)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=768, y=1320)
        else:
            return KeyboardName(x=344, y=1288)

    def SixEn(self) -> KeyboardName:
        """
        9键英文
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=127, y=1477)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=127, y=1477)
        else:
            return KeyboardName(x=562, y=1288)

    def Keyboard_Q(self) -> KeyboardName:
        """
        键盘Q
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=50, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=50, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x,
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=50, y=1100)

    def Keyboard_W(self) -> KeyboardName:
        """
        键盘Q
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=135, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=135, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + self.single_item_size.width,
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=135, y=1100)

    def Keyboard_E(self) -> KeyboardName:
        """
        键盘E
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=225, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=225, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (2 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=225, y=1100)

    def Keyboard_R(self) -> KeyboardName:
        """
        键盘R
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=315, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=315, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (3 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=315, y=1100)

    def Keyboard_T(self) -> KeyboardName:
        """
        键盘Q
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=407, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=407, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (4 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=407, y=1100)

    def Keyboard_Y(self) -> KeyboardName:
        """
        键盘Q
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=500, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=500, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (5 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=500, y=1100)

    def Keyboard_U(self) -> KeyboardName:
        """
        键盘Q
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=585, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=585, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (6 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=585, y=1100)

    def Keyboard_I(self) -> KeyboardName:
        """
        键盘I
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=677, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=677, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (7 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=677, y=1100)

    def Keyboard_O(self) -> KeyboardName:
        """
        键盘O
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=767, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=767, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (8 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=767, y=1100)

    def Keyboard_P(self) -> KeyboardName:
        """
        键盘P
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=855, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=855, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x + (9 * self.single_item_size.width),
                                y=self.key26_q.y)
        else:
            return KeyboardName(x=855, y=1100)

    def Keyboard_A(self) -> KeyboardName:
        """
        键盘A
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=95, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=95, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x,
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=95, y=1230)

    def Keyboard_S(self) -> KeyboardName:
        """
        键盘S
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=184, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=184, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + self.single_item_size.width,
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=184, y=1230)

    def Keyboard_D(self) -> KeyboardName:
        """
        键盘D
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=272, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=272, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (2 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=272, y=1230)

    def Keyboard_F(self) -> KeyboardName:
        """
        键盘F
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=362, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=362, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (3 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=362, y=1230)

    def Keyboard_G(self) -> KeyboardName:
        """
        键盘G
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=452, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=452, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (4 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=452, y=1230)

    def Keyboard_H(self) -> KeyboardName:
        """
        键盘H
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=540, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=540, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (5 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=540, y=1230)

    def Keyboard_J(self) -> KeyboardName:
        """
        键盘J
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=632, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=632, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (6 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=632, y=1230)

    def Keyboard_K(self) -> KeyboardName:
        """
        键盘K
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=720, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=720, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (7 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=720, y=1230)

    def Keyboard_L(self) -> KeyboardName:
        """
        键盘L
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=812, y=1260)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=812, y=1260)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_a.x + (8 * self.single_item_size.width),
                                y=self.key26_a.y)
        else:
            return KeyboardName(x=812, y=1230)

    def Keyboard_Z(self) -> KeyboardName:
        """
        键盘Z
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=182, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=182, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x,
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=179, y=1378)

    def Keyboard_X(self) -> KeyboardName:
        """
        键盘X
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=272, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=272, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x + self.single_item_size.width,
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=272, y=1378)

    def Keyboard_C(self) -> KeyboardName:
        """
        键盘C
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=364, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=364, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x + (2 * self.single_item_size.width),
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=364, y=1388)

    def Keyboard_V(self) -> KeyboardName:
        """
        键盘V
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=454, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=454, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x + (3 * self.single_item_size.width),
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=454, y=1388)

    def Keyboard_B(self) -> KeyboardName:
        """
        键盘B
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=540, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=540, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x + (4 * self.single_item_size.width),
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=540, y=1388)

    def Keyboard_N(self) -> KeyboardName:
        """
        键盘N
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=630, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=630, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x + (5 * self.single_item_size.width),
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=630, y=1388)

    def Keyboard_M(self) -> KeyboardName:
        """
        键盘M
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=722, y=1388)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=722, y=1388)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_z.x + (6 * self.single_item_size.width),
                                y=self.key26_z.y)
        else:
            return KeyboardName(x=722, y=1388)

    def Choose_Word(self) -> KeyboardName:
        """
        选词
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=206, y=1003)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=206, y=1003)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key26_q.x,
                                y=self.key26_q.y - (self.single_item_size.height/2))
        else:
            return KeyboardName(x=206, y=960)

    def Delete_Action(self,
                      keyboard_ime: KeyboardType) -> KeyboardName:
        """
        删除按钮
        :param keyboard_ime: 删除按钮在不同界面上位置不同
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            if keyboard_ime == KeyboardType.Keyboard26Key:
                return KeyboardName(x=838, y=1390)
            else:
                return KeyboardName(x=838, y=1138)
        elif self.keyboard_type == InputCom.Baidu:
            if keyboard_ime == KeyboardType.Keyboard26Key:
                return KeyboardName(x=838, y=1380)
            else:
                return KeyboardName(x=826, y=1128)
        elif self.keyboard_type == InputCom.IflytekReal:
            if keyboard_ime == KeyboardType.Keyboard26Key:
                return KeyboardName(x=self.key26_z.x + (7 * self.single_item_size.width),
                                    y=self.key26_z.y)
            else:
                return KeyboardName(x=self.key9_smell.x,
                                    y=self.key9_smell.y - self.single_item_9key_size.height)
        else:
            if keyboard_ime == KeyboardType.Keyboard26Key:
                return KeyboardName(x=824, y=1375)
            else:
                return KeyboardName(x=821, y=1086)

    def DownArrow_Action(self) -> KeyboardName:
        """
        下拉按键操作
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=850, y=1010)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=828, y=1013)
        else:
            return KeyboardName(x=824, y=960)

    def Keyboard_ABC(self) -> KeyboardName:
        """
        9键键盘ABC
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=450, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=450, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x + self.single_item_9key_size.width,
                                y=self.key9_smell.y)
        else:
            return KeyboardName(x=450, y=1100)

    def Keyboard_DEF(self) -> KeyboardName:
        """
        9键键盘DEF
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=650, y=1130)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=650, y=1130)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x + self.single_item_9key_size.width * 2,
                                y=self.key9_smell.y)
        else:
            return KeyboardName(x=650, y=1100)

    def Keyboard_GHI(self) -> KeyboardName:
        """
        9键键盘GHI
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=248, y=1258)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=248, y=1258)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x,
                                y=self.key9_smell.y + self.single_item_9key_size.height)
        else:
            return KeyboardName(x=248, y=1233)

    def Keyboard_JKL(self) -> KeyboardName:
        """
        9键键盘GHI
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=450, y=1258)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=450, y=1258)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x + self.single_item_9key_size.width,
                                y=self.key9_smell.y + self.single_item_9key_size.height)
        else:
            return KeyboardName(x=450, y=1233)

    def Keyboard_MNO(self) -> KeyboardName:
        """
        9键键盘MNO
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=650, y=1258)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=650, y=1258)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x + self.single_item_9key_size.width * 2,
                                y=self.key9_smell.y + self.single_item_9key_size.height)
        else:
            return KeyboardName(x=650, y=1233)

    def Keyboard_PQRS(self) -> KeyboardName:
        """
        9键键盘PQRS
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=250, y=1390)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=250, y=1390)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x,
                                y=self.key9_smell.y + self.single_item_9key_size.height * 2)
        else:
            return KeyboardName(x=250, y=1375)

    def Keyboard_TUV(self) -> KeyboardName:
        """
        9键键盘PQRS
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=450, y=1390)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=450, y=1390)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x + self.single_item_9key_size.width,
                                y=self.key9_smell.y + self.single_item_9key_size.height * 2)
        else:
            return KeyboardName(x=450, y=1375)

    def Keyboard_WXYZ(self) -> KeyboardName:
        """
        9键键盘WXYZ
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=650, y=1390)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=650, y=1390)
        elif self.keyboard_type == InputCom.IflytekReal:
            return KeyboardName(x=self.key9_smell.x + self.single_item_9key_size.width * 2,
                                y=self.key9_smell.y + self.single_item_9key_size.height * 2)
        else:
            return KeyboardName(x=650, y=1375)

    def Keyboard_Last_Word(self) -> KeyboardName:
        """
        显示位置的最后一位
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=750, y=1017)
        elif self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=709, y=1018)
        else:
            return KeyboardName(x=709, y=1018)

    @staticmethod
    def Keyboard_Baidu_NextPage() -> KeyboardName:
        """
        百度输入法下一个页面
        :return:
        """
        return KeyboardName(x=560, y=1544)

    def Keyboard_Return(self) -> KeyboardName:
        """
        下拉选词返回按钮
        :return:
        """
        if self.keyboard_type == InputCom.Baidu:
            return KeyboardName(x=800, y=1536)

    def Keyboard_Enter(self) -> KeyboardName:
        """
        点击回车按钮
        :return:
        """
        if self.keyboard_type == InputCom.Sogou:
            return KeyboardName(x=830, y=1524)
