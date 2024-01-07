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
# The script adds the following Wrapper functions to be used for the API tests:
- Request Method(s)
- Helpers (to load files etc.)
# ----------------------------------------------------------------------------
"""
import requests as re

from base_script import TestBase
from logger import logging_setup

logger = logging_setup()


# ----------------------------------------------- REQUEST Operations ---------------------------------------------#
#                                                                                                                 #
# ----------------------------------------------------------------------------------------------------------------#
def post_req(url, headers, api_data):
    """
    Sends a POST request with the specified parameters
    Args:
        url: the specific url of the request
        headers: Required Headers
        api_data: The request body to be sent

    Returns: a Rest object with all the properties to proceed for tests
    """
    resp_post = request_operation(req_method='POST', url=url, data=api_data, headers=headers)
    return resp_post


def get_req(url, headers):
    """
    Sends a POST request with the specified parameters
    Args:
        url: the specific url of the request
        headers: Required Headers

    Returns: a Rest object with all the properties to proceed for tests
    """
    resp_post = request_operation(req_method='GET', url=url, headers=headers)
    return resp_post


def request_operation(req_method, url, headers, data=None):
    """
    Method to send the api_tests request using the 'requests' library object.
    Args:
        req_method: specifies the method for the api_tests request to be sent i.e. GET or POST etc.
        url: the specific url of the request
        headers: Required Headers
        data: request body

    Returns: A Rest object with all the properties in the api_tests response to proceed
    """
    # url = f"{protocol}://{host}/{api_ver}{url}"

    try:
        logger.debug(f"Sending the {req_method} request to the URL: {url}")
        resp = re.request(req_method, url=url, json=data, headers=headers, timeout=120)
        return resp

    except re.exceptions.RequestException as ex:
        logger.error(f"Unknown exception occurred. Please check the logs for the details. \n {ex}")
