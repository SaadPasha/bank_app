from api_tests import req_setup
from logger import logging_setup

LOGGER = logging_setup()


def create_new_user(url, data, headers):
    create_user_resp = req_setup.post_req(url=url, api_data=data, headers=headers)
    if create_user_resp.status_code != 201:
        LOGGER.debug(f"User creation request unsuccessful. Response JSON: \n{create_user_resp.json()}")
    return create_user_resp
