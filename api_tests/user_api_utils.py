from api_tests import req_setup
from logger import logging_setup

LOGGER = logging_setup()


def create_new_user(url, data, headers):
    create_user_resp = req_setup.post_req(url=url, api_data=data, headers=headers)
    if create_user_resp.status_code != 201:
        LOGGER.debug(f"User creation request unsuccessful. Response JSON: \n{create_user_resp.json()}")
    return create_user_resp


def deposit_amount(url, data, headers):
    deposit_amount_resp = req_setup.post_req(url=url, api_data=data, headers=headers)
    if deposit_amount_resp.status_code !=201:
        LOGGER.debug(f"Deposit amount request unsuccessful. Response JSON: \n{deposit_amount_resp.json()}")
    return deposit_amount_resp