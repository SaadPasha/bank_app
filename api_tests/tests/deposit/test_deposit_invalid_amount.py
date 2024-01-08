from api_tests import user_api_utils
import allure


@allure.title("Deposit - BE - Invalid amount specified")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("The test case verifies that in case there's no amount specified in the JSON OR the amount is Zero (0), "
                    "then system generates an appropriate message and the request is not processed.")
def test_deposit_amount_success(config, deposit_data, user_data, create_user_url, deposit_amount_url, logger):
    """
    Test Case Function
    Args:
        config: Config fixture
        deposit_data: Test Data fixture
        deposit_amount_url: Deposit API URL Fixture
        logger: Logger Fixture

    Returns: None
    """
    # Pre-Condition -> Create User
    new_user_amount_invalid = user_api_utils.create_new_user(url=create_user_url, data=user_data, headers=config.headers).json()['generated_user_id']
    deposit_data['user_id'] = new_user_amount_invalid

    with allure.step("Send a POST request to the endpoint: /deposit with the 'amount' set to zero (0)."):
        invalid_deposit_amount_data = deposit_data.copy()
        invalid_deposit_amount_data['amount'] = 0

        invalid_deposit_amount_data_resp = user_api_utils.deposit_amount(url=deposit_amount_url, data=invalid_deposit_amount_data, headers=config.headers)
        assert invalid_deposit_amount_data_resp.status_code == 400
        assert invalid_deposit_amount_data_resp.json()['status'] == "failed"
        assert invalid_deposit_amount_data_resp.json()['error']['message'] == "Invalid parameter value: 'amount'"
        assert invalid_deposit_amount_data_resp.json()['error']['details'] == "Input should be greater than 0"

        logger.info(f"The HTTP response code is 400 with the following details:\n{invalid_deposit_amount_data_resp.json()}")

    with allure.step("Send a POST request to the endpoint: /deposit with no 'amount' key"):
        missing_user_id_data = deposit_data.copy()
        missing_user_id_data.pop('amount', None)

        missing_user_id_data_resp = user_api_utils.deposit_amount(url=deposit_amount_url, data=missing_user_id_data, headers=config.headers)
        assert missing_user_id_data_resp.status_code == 400
        assert missing_user_id_data_resp.json()['status'] == "failed"
        assert missing_user_id_data_resp.json()['error']['message'] == "Invalid parameter value: 'amount'"
        assert missing_user_id_data_resp.json()['error']['details'] == "Field required"
