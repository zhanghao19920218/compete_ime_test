# coding=utf-8
"""
@File    : entrance.py
@Time    : 2022/6/14 14:35
@Author  : haozhang45
@Email   : haozhang45@iflytek.com
@Software : PyCharm
@Description: Run multi core task
"""
from utils import run_multicore

if __name__ == '__main__':
    run_multicore("python3", "main.py", [0, 1])
