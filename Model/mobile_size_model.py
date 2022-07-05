# coding=utf-8
# @author: haozhang45
# @date: 2022/4/15
# @description: 读取真机屏幕的model
import json
import os

from constant import MOBILE_SIZE_JSON_PATH


class CoordinateModel(object):
    """
    坐标位置
    """
    x: int = 0

    y: int = 0

    def __init__(self,
                 x: int,
                 y: int):
        self.x = x
        self.y = MobileSizeModel.get_screen_height() - MobileSizeModel.get_start_y() + y

    @staticmethod
    def dict_to_object(d: dict):
        """
        从字典转化成Model
        :param d:
        :return:
        """
        return CoordinateModel(
            x=d.get('x') if 'x' in d else 0,
            y=d.get('y') if 'y' in d else 0
        )


class ItemSizeModel(object):
    """
    按钮的位置
    """
    width: int = 0

    height: int = 0

    def __init__(self,
                 width: int,
                 height: int):
        self.width = width
        self.height = height

    @staticmethod
    def dict_to_object(d: dict):
        """
        将字典转为model
        :param d:
        :return:
        """
        return ItemSizeModel(
            width=d.get('width'),
            height=d.get('height')
        )


class Keys9keyModel(object):
    """
    Model for 9key
    """
    keys_smell: CoordinateModel = None

    single_item: ItemSizeModel = None

    def __init__(self,
                 keys_smell: CoordinateModel,
                 single_item: ItemSizeModel):
        self.single_item = single_item
        self.keys_smell = keys_smell

    @staticmethod
    def dict_to_object(d: dict):
        """
        Convert dictionary to model
        :param d:
        :return:
        """
        return Keys9keyModel(
            keys_smell=CoordinateModel.dict_to_object(d.get("smell")),
            single_item=ItemSizeModel.dict_to_object(d.get("single_item"))
        )


class Keys26keyModel(object):
    """
    26键的Model
    """
    keys_q: CoordinateModel = None

    keys_a: CoordinateModel = None

    keys_z: CoordinateModel = None

    single_item: ItemSizeModel = None

    def __init__(self,
                 keys_q: CoordinateModel,
                 keys_a: CoordinateModel,
                 keys_z: CoordinateModel,
                 single_item: ItemSizeModel):
        self.keys_q = keys_q
        self.keys_a = keys_a
        self.keys_z = keys_z
        self.single_item = single_item

    @staticmethod
    def dict_to_object(d: dict):
        """
        将字典转为model
        :param d:
        :return:
        """
        return Keys26keyModel(
            keys_q=CoordinateModel.dict_to_object(d.get("Q")),
            keys_a=CoordinateModel.dict_to_object(d.get("A")),
            keys_z=CoordinateModel.dict_to_object(d.get("Z")),
            single_item=ItemSizeModel.dict_to_object(d.get("single_item"))
        )


class KeyboardsDetailModel(object):
    """
    详细的Model
    """
    menu_key: CoordinateModel = None  # 菜单位置

    setting_key: CoordinateModel = None  # 详细设置位置

    all_setting: CoordinateModel = None  # 设置里面的全部设置按钮

    pinyin_26key: CoordinateModel = None  # 26键拼音位置

    pinyin_9key: CoordinateModel = None  # 9键拼音位置

    keys_26key: Keys26keyModel = None  # 26键按钮位置

    keys_9key: Keys9keyModel = None  # Keyboard for 9 key

    def __init__(self,
                 menu_key: CoordinateModel,
                 pinyin_26key: CoordinateModel,
                 pinyin_9key: CoordinateModel,
                 keys_26key: Keys26keyModel,
                 keys_9key: Keys9keyModel,
                 setting_key: CoordinateModel,
                 all_setting: CoordinateModel):
        self.menu_key = menu_key
        self.pinyin_9key = pinyin_9key
        self.pinyin_26key = pinyin_26key
        self.keys_26key = keys_26key
        self.keys_9key = keys_9key
        self.setting_key = setting_key
        self.all_setting = all_setting

    @staticmethod
    def dict_to_object(d: dict):
        """
        将字典转为model
        :param d:
        :return:
        """
        return KeyboardsDetailModel(
            menu_key=CoordinateModel.dict_to_object(d.get("keyboards").get("menu_key")),
            pinyin_9key=CoordinateModel.dict_to_object(d.get("keyboards").get("pinyin_9key")),
            pinyin_26key=CoordinateModel.dict_to_object(d.get("keyboards").get("pinyin_26key")),
            keys_26key=Keys26keyModel.dict_to_object(d.get("keyboards").get("keys_26key")),
            keys_9key=Keys9keyModel.dict_to_object(d.get("keyboards").get("keys_9key")),
            setting_key=CoordinateModel.dict_to_object(d.get("keyboards").get("setting")),
            all_setting=CoordinateModel.dict_to_object(d.get("keyboards").get("all_setting"))
        )


class MobileSizeModel(object):
    """
    解析json格式
    """

    wid_1080_model: KeyboardsDetailModel = None
    start_y: int = 0
    _screen_height = 0

    def __init__(self,
                 wid_1080: KeyboardsDetailModel):
        self.wid_1080_model = wid_1080

    @staticmethod
    def get_start_y():
        """
        获取起始的y轴
        :return:
        """
        return MobileSizeModel.start_y

    @staticmethod
    def set_screen_height(screen_height: int):
        """
        设置静态变量
        :param screen_height: 屏幕高度
        :return:
        """
        MobileSizeModel._screen_height = screen_height

    @staticmethod
    def get_screen_height() -> int:
        """
        获取屏幕高度
        :return:
        """
        return MobileSizeModel._screen_height

    @staticmethod
    def json_to_object(screen_height: int):
        """
        将字典转为model
        :param screen_height: 屏幕的高度
        :return:
        """
        current_path: str = os.getcwd()  # 当前路径
        json_file_path: str = MOBILE_SIZE_JSON_PATH
        MobileSizeModel.set_screen_height(screen_height=screen_height)
        d: dict
        with open(file=json_file_path,
                  mode='rt',
                  encoding="utf-8") as json_file:
            d = json.load(json_file)
            MobileSizeModel.start_y = int(d.get("wid_1080").get("height"))
        return MobileSizeModel(
            wid_1080=KeyboardsDetailModel.dict_to_object(d=d.get("wid_1080"))
        )
