# coding=utf-8
# @author: haozhang45
# @date: 2022/2/23
# @description: Packaging the adb by python, run command like connect devices; get devices
import time
from socket import socket

from Parameter import InputCom
from constant import IFLYTEK_APK, SOGOU_APK, IFLYTEK_PACKAGENAME, SOGOU_PACKAGENAME, IME_PACKAGENAME, BAIDU_PACKAGENAME
from adbutils import AdbClient, AdbDevice, Network, WindowSize
from typing import List
import os


class BAADB(object):
    """
    对adb进行二次封装
    """
    adb = None

    device = None

    device_name: str = ""

    def __init__(self,
                 device_name: str):
        """
        链接的设备名
        :param device_name:
        """
        self.adb = AdbClient(host="127.0.0.1", port=5037)
        self.device_name = device_name
        self.device = self.adb.device(serial=self.device_name)

    def get_screen_size(self) -> WindowSize:
        """
        获取屏幕长宽
        :return:
        """
        return self.device.window_size()

    def connect_device(self):
        """
        链接mumu模拟器, 或者真机
        :return:
        """
        device_models: List[AdbDevice] = self.adb.device_list()
        device_names: List[str] = list(map(lambda item: item.get_serialno(), device_models))
        if self.device_name not in device_names:
            self.adb.connect(self.device_name)
        else:
            print(f"{self.device_name} Already Connect")

    def create_connection(self,
                          socket_port: int) -> socket:
        """
        创建一个手机链接
        :param socket_port: socket链接端口号
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        w_socket: socket = self.device.create_connection(network=Network.TCP,
                                                         address=socket_port)
        return w_socket

    def socket_shell(self,
                     socket_port: int):
        """
        运行设备的一个shell
        :param socket_port:
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        self.device.shell(f"forward tcp:9999 tcp:{socket_port}")

    def install_apk(self,
                    apk_type: InputCom):
        """
        运行adb的指令
        :param apk_type: 搜狗还是讯飞输入法
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        if apk_type == InputCom.Sogou:
            sogou_apk_path: str = os.path.abspath(os.path.join(os.getcwd(), "..", "apk", SOGOU_APK))
            if not os.path.exists(sogou_apk_path):
                raise FileNotFoundError
            else:
                self.device.install(sogou_apk_path)
        else:
            iflytek_apk_path: str = os.path.abspath(os.path.join(os.getcwd(), "..", "apk", IFLYTEK_APK))
            if not os.path.exists(iflytek_apk_path):
                raise FileNotFoundError
            else:
                self.device.install(iflytek_apk_path)

    def uninstall_apk(self,
                      apk_type: InputCom):
        """
        卸载应用
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        if apk_type == InputCom.Sogou:
            self.device.uninstall(pkg_name=SOGOU_PACKAGENAME)
        else:
            self.device.uninstall(pkg_name=IFLYTEK_APK)

    def set_privilege(self,
                      apk_type: InputCom):
        """
        设置输入法权限
        :param apk_type: 搜狗或者讯飞输入法
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        package_name: str = BAADB.get_package_name(apk_type=apk_type)
        self.device.shell(f"pm grant {package_name} android.permission.WRITE_EXTERNAL_STORAGE")
        self.device.shell(f"pm grant {package_name} android.permission.READ_EXTERNAL_STORAGE")
        self.device.shell(f"pm grant {package_name} android.permission.READ_PHONE_STATE")
        self.device.shell(f"pm grant {package_name} android.permission.READ_CONTACTS")
        self.device.shell(f"pm grant {package_name} android.permission.RECORD_AUDIO")
        self.device.shell(f"pm grant {package_name} android.permission.ACCESS_COARSE_LOCATION")
        self.device.shell(f"pm grant {package_name} android.permission.ACCESS_FINE_LOCATION")
        self.device.shell(f"pm grant {package_name} android.permission.CAMERA")

    def set_ime(self,
                apk_type: InputCom):
        """
        设置手机输入法
        :param apk_type:
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        package_name: str = BAADB.get_package_name(apk_type=apk_type)
        self.device.shell(f"ime enable {package_name}")
        self.device.shell(f"ime set {package_name}")

    def kill_apk(self):
        """
        关闭输入应用
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        self.device.shell(f"am force-stop {IME_PACKAGENAME}")
        time.sleep(1)

    @staticmethod
    def get_package_name(apk_type: InputCom) -> str:
        """
        获取包名称
        :param apk_type: 输入法type
        :return:
        """
        if apk_type == InputCom.IflyTek or apk_type == InputCom.IflytekReal:
            package_name: str = f"{IFLYTEK_PACKAGENAME}/.FlyIME"
        elif apk_type == InputCom.Baidu:
            package_name: str = f"{BAIDU_PACKAGENAME}/.ImeService"
        else:
            package_name: str = f"{SOGOU_PACKAGENAME}/.SogouIME"
        return package_name

    def start_ime_test(self):
        """
        启动测试apk
        :return:
        """
        self.device = self.adb.device(serial=self.device_name)
        self.device.app_start(package_name=IME_PACKAGENAME, activity=f"{IME_PACKAGENAME}.MainActivity")


if __name__ == '__main__':
    adb_con: BAADB = BAADB(device_name=DEVICE_NAME)
    adb_con.connect_device()
    # adb_con.uninstall_apk(apk_type=InputCom.Sogou)
    # adb_con.install_apk(apk_type=InputCom.Sogou)
    # adb_con.set_privilege(apk_type=InputCom.Sogou)
    adb_con.set_ime(apk_type=InputCom.Sogou)
    adb_con.start_ime_test()
