# 根据文件路径生成该文件的md5值

# coding=utf-8

import hashlib
import sys
import os


def get_filemd5(file_path):
    # 处理文件是否存在判断
    if os.path.exists(file_path):
        # 执行md5操作
        return get_file_md5(file_path)
    else:
        print('请先确保文件路径正确')


def md5_convert(string):
    """计算字符串md5值
    :param string: 输入字符串
    :return: 字符串md5
    """
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()


def get_file_md5(file_path):
    """获取文件md5值
    :param file_path: 文件路径名
    :return: 文件md5值
    """
    with open(file_path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).lower()
