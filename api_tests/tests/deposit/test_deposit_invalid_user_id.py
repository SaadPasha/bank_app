from api_tests import user_api_utils
import allure


@allure.title("Deposit - BE - Missing/Invalid user ID")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("The test case verifies that in case a missing/invalid user ID is sent in the payload,"
                    " then the system doesn't processes the request and an appropriate error code is generated.")
def test_deposit_amount_invalid_user_id(config, deposit_data, user_data, create_user_url, deposit_amount_url, logger):
    """
    Test Case Function
    Args:
        config: Config fixture
        deposit_data: Test Data fixture
        deposit_amount_url: Deposit API URL Fixture
        logger: Logger Fixture

    Returns: None
    """

    with allure.step("Send a POST request to the endpoint: /deposit with the invalid user ID"):
        invalid_deposit_data = deposit_data.copy()
        invalid_deposit_data['user_id'] = 100001

        invalid_deposit_user_id_resp = user_api_utils.deposit_amount(url=deposit_amount_url, data=invalid_deposit_data, headers=config.headers)
        assert invalid_deposit_user_id_resp.status_code == 400
        assert invalid_deposit_user_id_resp.json()['status'] == "failed"
        assert invalid_deposit_user_id_resp.json()['error']['message'] == "Invalid parameter value: 'user_id'"
        assert invalid_deposit_user_id_resp.json()['error']['details'] == "Input should be a valid string"

        logger.info(f"The HTTP response code is 400 with the following details:\n{invalid_deposit_user_id_resp.json()}")

    with allure.step("Send a POST request to the endpoint: /deposit with no user_id key"):
        missing_user_id_data = deposit_data.copy()
        missing_user_id_data.pop('user_id', None)

        missing_user_id_data_resp = user_api_utils.deposit_amount(url=deposit_amount_url, data=missing_user_id_data, headers=config.headers)
        assert missing_user_id_data_resp.status_code == 400
        assert missing_user_id_data_resp.json()['status'] == "failed"
        assert missing_user_id_data_resp.json()['error']['message'] == "Invalid parameter value: 'user_id'"
        assert missing_user_id_data_resp.json()['error']['details'] == "Field required"
