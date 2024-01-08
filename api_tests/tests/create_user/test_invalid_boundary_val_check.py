import pytest

from api_tests import user_api_utils
from api_tests import api_helpers
import allure


@allure.title("Create User - BE - Validation Checks")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("The test case verifies that when a POST request is sent to the endpoint: /create_user - with the improper payload, "
                    "then the system generates an error message and the request is not processed.")
@pytest.mark.parametrize("key, boundary_val", [("f_name", 1), ("f_name", 256), ("l_name", 1), ("l_name", 256),
                                               ("phone", 5), ("phone", 15), ("email", 3)])
def test_create_new_user(config, user_data, create_user_url, logger, key, boundary_val):
    """
    Test Case Function
    Args:
        config: Config fixture
        user_data: Test Data fixture
        create_user_url: Generate API URL Fixture
        logger: Logger Fixture

    Returns: None
    """
    if key != 'email':
        with allure.step(f"Send a POST request to the API endpoint: /create_user with the out of boundary value of '{boundary_val}' chars for the '{key}' key"):
            boundary_val_data = user_data.copy()
            boundary_value_string = api_helpers.gen_rand_str(boundary_val)

            boundary_val_data[key] = boundary_value_string

            create_user_boundary_value = user_api_utils.create_new_user(url=create_user_url, data=boundary_val_data, headers=config.headers)

            assert create_user_boundary_value.status_code == 400
            assert create_user_boundary_value.json()['status'] == "failed"
            assert create_user_boundary_value.json()['error']['message'] == f"Invalid parameter value: '{key}'"

            logger.info(f"The response is the status code of HTTP 400 with the following JSON body: {create_user_boundary_value.json()}")

    else:
        with allure.step("Send a POST request to the API endpoint: /create_user with the less than 6 email chars"):
            six_char_email_data = user_data.copy()
            less_than_char_email = "j@e.co"

            six_char_email_data['email'] = less_than_char_email

            less_than_char_email_req = user_api_utils.create_new_user(url=create_user_url, data=six_char_email_data, headers=config.headers)

            assert less_than_char_email_req.status_code == 400
            assert less_than_char_email_req.json()['status'] == "failed"
            assert less_than_char_email_req.json()['error']['message'] == "Invalid parameter value: 'email'"
            assert less_than_char_email_req.json()['error']['details'] == "Value should have at least 8 items after validation, not 6"

        with allure.step("Send a POST request to the API endpoint: /create_user with the incorrect email format"):
            incorrect_email = "johndoe.com"
            incorrect_email_data = user_data.copy()

            incorrect_email_data['email'] = incorrect_email

            incorrect_email_req = user_api_utils.create_new_user(url=create_user_url, data=incorrect_email_data, headers=config.headers)

            assert incorrect_email_req.status_code == 400
            assert incorrect_email_req.json()['status'] == "failed"
            assert incorrect_email_req.json()['error']['message'] == "Invalid parameter value: 'email'"
            assert incorrect_email_req.json()['error']['details'] == "value is not a valid email address: The email address is not valid. It must have exactly one @-sign."