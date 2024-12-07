import argparse
import os
import logging
from datetime import datetime
from src import img_convert
from configs import default_modes, total_modes

def handler(file_path, link=True):
    if link:
        res = []
        res.append(img_convert(file_path, os.path.dirname(os.getcwd()), link=True))
        attend_log(res)
        return str(res)

def attend_log(log_list):


    # 配置日志格式
    log_format = '%(asctime)s - %(message)s'
    date_format = '%Y:%m:%d:%H:%M:%S'

    # 创建一个logger
    logger = logging.getLogger('example_logger')
    logger.setLevel(logging.DEBUG)  # 设置日志级别

    # 创建一个文件处理器，并设置级别为DEBUG
    file_handler = logging.FileHandler('Upload.log')
    file_handler.setLevel(logging.DEBUG)

    # 创建一个流处理器，用于输出到控制台，可选
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    # 创建一个日志格式器，并设置格式
    formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # 将文件处理器和流处理器添加到logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # 写入日志
    logger.debug(log_list)
