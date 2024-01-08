import pytest

from api_tests import user_api_utils
import allure


@allure.title("Create User - BE - Invalid Payload")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("The test case verifies that when a POST request is sent to the endpoint: /create_user - with the Invalid payload,"
                    " then a new user is NOT created and the system generates an error message specifying the problem.")
@pytest.mark.parametrize("invalid_key, invalid_value", [("f_name", 123), ("l_name", 123), ("dob", "19-02-1996"),
                                                        ("email", "johndoe.com"), ("address", 1245), ("phone", 12345)])
def test_create_user_invalid_payload(config, user_data, create_user_url, logger, invalid_key, invalid_value):
    """
    Test Case Function
    Args:
        config: Config fixture
        user_data: Test Data fixture
        create_user_url: Generate API URL Fixture
        logger: Logger Fixture

    Returns: None
    """
    with allure.step(f"Send a POST request to the API endpoint: /create_user with Invalid datatype for the {invalid_key} key."):
        invalid_user_data = user_data.copy()
        invalid_user_data[invalid_key] = invalid_value

        create_user_invalid_key = user_api_utils.create_new_user(url=create_user_url, data=invalid_user_data, headers=config.headers)
        assert create_user_invalid_key.status_code == 400
        assert create_user_invalid_key.json()['status'] == "failed"
        assert create_user_invalid_key.json()['error']['message'] == f"Invalid parameter value: '{invalid_key}'"

        logger.info(f"The response is the status code of HTTP 400 with the following JSON body: {create_user_invalid_key.json()}")
