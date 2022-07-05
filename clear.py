import os
import json
import shutil
from typing import List

writer_logs_path = os.getcwd() + "/logs/"
writer_full_logs_path = os.getcwd() + "/full_logs/"
check_error_correct_writer_path = os.getcwd() + "/checks/"
check_all_error_correct_writer_path = os.getcwd() + "/checks_all/"
temp_file_index = os.path.abspath(os.path.join(os.getcwd(), 'index_info'))
errors_file_path = os.getcwd() + "/test/"
cloud_logs_path = os.getcwd() + "/apk_info_logs/"


def clear_file():
    """
    清除当前总进度
    :return:
    """
    if os.path.exists(temp_file_index):
        list_logs: List[str] = os.listdir(temp_file_index)
        for file in list_logs:
            os.remove(os.path.abspath(os.path.join(temp_file_index, file)))
            print("{filename} 内容清除完成！".format(filename=(temp_file_index + "/" + file)))

    if os.path.exists(writer_logs_path):
        list_files = os.listdir(writer_logs_path)
        for dir_name in list_files:
            if dir_name.endswith(".txt"):
                os.remove(os.path.abspath(os.path.join(writer_logs_path, dir_name)))
            else:
                shutil.rmtree(os.path.abspath(os.path.join(writer_logs_path, dir_name)))

    # 清除输入文件夹
    # list_errors = os.listdir(errors_file_path)
    # for file in list_errors:
    #     os.remove(errors_file_path + "/" + file)

    # 清除输出文件夹
    if os.path.exists(writer_logs_path):
        list_logs = os.listdir(writer_logs_path)
        for file in list_logs:
            os.remove(writer_logs_path + "/" + file)
            print("{filename} 删除完成！".format(filename=file))

    # 清除输出文件夹
    if os.path.exists(writer_full_logs_path):
        list_logs = os.listdir(writer_full_logs_path)
        for file in list_logs:
            os.remove(writer_full_logs_path + "/" + file)
            print("{filename}  full删除完成！".format(filename=file))

    # 清除云端结果
    if os.path.exists(cloud_logs_path):
        list_logs = os.listdir(cloud_logs_path)
        for file in list_logs:
            os.remove(cloud_logs_path + "/" + file)
            print("{filename}  云端删除完成！".format(filename=file))


if __name__ == '__main__':
    clear_file()
