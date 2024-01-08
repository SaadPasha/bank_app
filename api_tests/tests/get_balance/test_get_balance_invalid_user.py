from api_tests import user_api_utils
import allure


@allure.title("Balance - BE - Incorrect/Invalid user id")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("The test case verifies that in case a incorrect/invalid user ID is sent in the headers,"
                    " then the system doesn't processes the request and an appropriate error code is generated.")

def test_deposit_amount_success(config, get_balance_url, logger):
    """
    Test Case Function
    Args:
        config: Config fixture
        get_balance_url: Get Balance API URL fixture
        logger: Logger Fixture

    Returns: None
    """
    with allure.step("Send a GET request to the endpoint: /get_balance with the invalid user ID in query param"):
        get_balance_url = get_balance_url +"/" + "abc124"
        invalid_get_balance_resp = user_api_utils.get_balance(url=get_balance_url, headers=config.headers)
        assert invalid_get_balance_resp.status_code == 404
        assert invalid_get_balance_resp.json()['detail']['status'] == "failed"
        assert invalid_get_balance_resp.json()['detail']['error']['message'] == "User not found"
        assert invalid_get_balance_resp.json()['detail']['error']['details'] == "The requested user with the provided ID does not exist. Please check the user ID and try again."

        logger.info(f"The HTTP response code is 404 with the following details:\n{invalid_get_balance_resp.json()}")


