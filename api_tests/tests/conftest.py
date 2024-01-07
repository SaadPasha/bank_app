from base_script import TestBase
from api_tests.api_data.user_params import UserParams
from logger import logging_setup

import pytest

@pytest.fixture(scope="session", autouse=True)
def config():
    config_loader = TestBase()
    return config_loader


@pytest.fixture(scope="function")
def create_user_url(config):
    user_url = config.api_web_protocol + "://" + config.api_web_host + "" + config.users_endpoint
    return user_url


@pytest.fixture(scope="function")
def user_data():
    return UserParams().gen_user_data()


@pytest.fixture(scope="session")
def logger():
    logger = logging_setup()
    return logger