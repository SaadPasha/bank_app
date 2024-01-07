#!/usr/bin/env python3
"""
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
__author__: "Saad Tahir"
__date__: "22/3/2022"
__updated__:
__version__ = "1.0"
__maintainer__ = "Saad Tahir"
__email__ = "saad.tahir@ut.ee"
__status__ = "Developed"
# ----------------------------------------------------------------------------
# The script adds the custom logging feature for the test automation framework.
# ----------------------------------------------------------------------------
"""
import os.path
import datetime
import logging
from base_script import TestBase

tb = TestBase()


def logging_setup(log_level=tb.log_level, log_dir_name=tb.log_dir_name, file_mode=tb.file_write_mode):
    """
    The function sets up the logging feature with the customized handler and formatter
    for the logs.
    Args:
        log_level: The min Log level to be used e.g. DEBUG or INFO
        log_dir_name: Name of the log directory to store logs
        file_mode: Enable writing logs to a file

    Returns: The 'logger' object for adding the logs
    """
    log_level = log_level.upper()
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s: [%(levelname)s] %(filename)s [%(funcName)s:%(lineno)d]: %(message)s")

    if not len(logger.handlers):
        if file_mode:
            _file_handler(logger=logger, log_level=log_level, formatter=formatter,
                          log_dir_name=log_dir_name)

        _std_handler(logger=logger, log_level=log_level, formatter=formatter)
    return logger


def _std_handler(logger, log_level, formatter):
    """
    Function to add standard console handler
    Args:
        logger: logger object of the logging class
        log_level: identifies the log level passed
        formatter: specifies the format of the log message

    Returns: Handler object to add logs to the console
    """
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(formatter)
    return logger.addHandler(stdout_handler)


def _file_handler(logger, log_level, formatter, log_dir_name):
    """
    Function to add File Log handler
    Args:
        logger: logger object of the logging class
        log_level: identifies the log level passed
        formatter: specifies the format of the log message
        log_dir_name: the name specified for the logs folder
    Returns: Handler object to add logs to the specified file
    """
    log_file_path = ""
    log_dir_path = os.path.join(os.path.dirname(__file__), log_dir_name)
    loge_file_name = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)
    if not os.path.isfile(loge_file_name):
        log_file_name = loge_file_name
        log_file_path = log_dir_path + "/" + log_file_name + ".log"

    file_handler = logging.FileHandler(log_file_path, mode='a')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    return logger.addHandler(file_handler)