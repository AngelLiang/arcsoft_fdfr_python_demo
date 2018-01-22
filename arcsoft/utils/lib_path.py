# coding=utf-8

import os

# 获取上级目录的绝对路径
last_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# 获取lib
LIB_DIR = os.path.join(last_dir, u"lib")

LINUX_X64_DIR = os.path.join(LIB_DIR, u"linux_x64")
WINDOWS_DIR = os.path.join(LIB_DIR, u"windows")
WIN32_DIR = os.path.join(LIB_DIR, u"win32")
WIN64_DIR = os.path.join(LIB_DIR, u"win64")

def test():
    print(LIB_DIR)
    print(LINUX_X64_DIR)
    print(WIN32_DIR)

if __name__ == '__main__':
    test()
