import pytest

from api_tests import user_api_utils
import allure


@allure.title("Create User - BE - Missing required fields")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("The test case verifies that when a POST request is sent to the endpoint: /create_user - with Missing required fields in the payload, "
                    "then a new user is NOT created and the system generates an error message specifying the problem.")

@pytest.mark.parametrize("missing_key", ["f_name", "l_name", "dob", "email", "address", "phone"])
def test_create_user_missing_fields(config, user_data, create_user_url, logger, missing_key):
    """
    Test Case Function
    Args:
        config: Config fixture
        user_data: Test Data fixture
        create_user_url: Generate API URL Fixture
        logger: Logger Fixture

    Returns: None
    """

    with allure.step(f"Send a POST request to the API endpoint: /create_user with with missing the key '{missing_key}' in the object"):
        missing_key_user_data = user_data.copy()
        missing_key_user_data.pop(missing_key, None)

        create_user_missing_key = user_api_utils.create_new_user(url=create_user_url, data=missing_key_user_data, headers=config.headers)

        assert create_user_missing_key.status_code == 400
        assert create_user_missing_key.json()['status'] == "failed"
        assert create_user_missing_key.json()['error']['message'] == f"Invalid parameter value: '{missing_key}'"
        assert create_user_missing_key.json()['error']['details'] == "Field required"

        logger.info(f"The response is the status code of HTTP 400 with the following JSON body: {create_user_missing_key.json()}")
