#!/usr/bin/env python3
"""
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
__author__: "Saad Tahir"
__date__: "22/3/2023"
__updated__: ""
__version__ = "1.0"
__maintainer__ = "Saad Tahir"
__email__ = "saad.tahir@ut.ee"
__status__ = "Developed"
# ----------------------------------------------------------------------------
# The script adds the Config Loader class for developing the API test scripts. It adds
# the support for following task(s):
# - Loading the config file
# - Initializing the config api_data
# ----------------------------------------------------------------------------
"""
import json
import os

class TestBase:
    """
    The Base class for the api_tests test scripts to load config
    """

    def __init__(self):
        # Loading the config api_data
        self.config_data = self.load_json()

        # Loading Host config api_data
        self.api_host_config_data = self.config_data.get('api_host_config')
        self.api_web_protocol = self.api_host_config_data.get('api_web_protocol')
        self.api_web_host = self.api_host_config_data.get('api_web_host')
        self.api_web_ver = self.api_host_config_data.get('api_web_ver')

        # Loading Headers
        self.headers = self.config_data.get('headers')
        self.headers_content_type = self.headers.get('Content-Type')

        # Loading api_tests endpoint
        self.users_endpoint = self.config_data.get('api_endpoint').get('create_user')
        self.deposit_endpoint = self.config_data.get('api_endpoint').get('deposit')

        # Custom Logger
        self.log_level = self.config_data.get('log_settings').get('log_level')
        self.log_dir_name = self.config_data.get('log_settings').get('log_dir_name')
        self.file_write_mode = self.config_data.get('log_settings').get('file_write_mode')

    @staticmethod
    def load_json():
        """
        Loads the JSON config file
        Returns: The config file api_data as dict
        """
        config_file_path = os.path.join(os.path.dirname(__file__), 'base_config.json')

        with open(file=config_file_path, mode='r', encoding='utf-8') as file:
            config_data = json.load(file)
        return config_data
