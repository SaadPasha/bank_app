from api_tests import user_api_utils
import allure


@allure.title("Create new User - Valid Credentials")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("The test case verifies that when a POST request is sent to the endpoint: /create_user - with the valid payload,"
                    "then a new user is created successfully with the respective details and the system generates a unique ID for it.")
def test_create_new_user(config, user_data, create_user_url, logger):
    """
    Test Case Function
    Args:
        config: Config fixture
        user_data: Test Data fixture
        create_user_url: Generate API URL Fixture
        logger: Logger Fixture

    Returns: None
    """
    with allure.step("Send a POST request to the API endpoint: /create_user"):
        create_user = user_api_utils.create_new_user(url=create_user_url, data=user_data, headers=config.headers)
        assert create_user.status_code == 201
        logger.info(f"User created successfully with the following creds:\n{create_user.json()}")
