# ----------------------------------------------- Helpers --------------------------------------------------------#
#                                                                                                                 #
# ----------------------------------------------------------------------------------------------------------------#
import json
import os
import random
import string

from jsonschema.validators import validate

from logger import logging_setup

logger = logging_setup()

def load_valid_schema(file_name):
    """
    Loads the validation schema file
    Args:
        file_name: The name of the JSON file

    Returns: a file object
    """
    try:
        file_path = os.path.join(os.path.join(os.path.dirname(__file__), "api_tests/loan_calc_schema"), file_name)
        with open(file_path, mode="r") as schema_file:
            schema = json.loads(schema_file.read())
            return schema

    except Exception as e:
        logger.error("Failed to load JSON schema file!\n{}".format(e))


def assert_schema(resp_data, schema_file_name="calculate_resp_valid.json"):
    """
    Asserts that the input schema is according the loaded JSON schema
    Args:
        resp_data: The JSON of the API response
        schema_file_name: Pre-Defined schema file name

    Returns: True
    """
    valid_schema = load_valid_schema(file_name=schema_file_name)
    return validate(resp_data, schema=valid_schema)


def gen_rand_int(min_length, max_length) -> int:
    """
    Generates a random ID to be used for creating a user
    Args:
        min_length: Min length of the integer
        max_length: Max length of the integer
    Returns: An int value
    """
    rand_int = random.randrange(min_length, max_length)
    logger.debug(f"Generated random integer: {rand_int} with {len(str(rand_int))} chars")
    return rand_int


def gen_rand_str(length) -> str:
    """
    Generates a random str to be used for creating a user
    Args:
        length: Max length of str

    Returns: A str value
    """
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))
    logger.debug(f"Generated random string: {rand_str} with {len(rand_str)} chars")
    return rand_str


# def invalid_req_methods(req_method, uri):
#     """
#     Sends the API requests using incorrect methods
#     Args:
#         req_method:
#         uri:
#
#     Returns:
#
#     """
#     resp_invalid_methods = request_operation(req_method=req_method, uri=uri, protocol=tb.api_web_protocol, host=tb.api_web_host,
#                                              api_data=None, api_ver=tb.api_ver, headers=tb.headers)
#     return resp_invalid_methods
