from api_tests import user_api_utils
import allure


@allure.title("Deposit - BE - Successful deposit")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("The test case verifies that in case a POST request is sent to the endpoint: /deposit - with the valid JSON payload, "
                    "then the system processes the request and credits the specific account with the specific amount.")
def test_deposit_amount_success(config, deposit_data, user_data, create_user_url, deposit_amount_url, logger):
    """
    Test Case Function
    Args:
        config: Config fixture
        deposit_data: Test Data fixture
        user_data: Test Data fixture
        create_user_url: User Creation API URL Fixture
        deposit_amount_url: Deposit API URL Fixture
        logger: Logger Fixture

    Returns: None
    """
    # Pre-Condition -> Create User
    new_user = user_api_utils.create_new_user(url=create_user_url, data=user_data, headers=config.headers).json()['generated_user_id']
    deposit_data['user_id'] = new_user

    with allure.step("Send a POST request to the endpoint: /deposit with the payload specified in the data field."):
        deposit_amount_resp = user_api_utils.deposit_amount(url=deposit_amount_url, data=deposit_data, headers=config.headers)
        assert deposit_amount_resp.status_code == 201
        assert deposit_amount_resp.json()['status'] == "success"
        assert deposit_amount_resp.json()['message'] == "Deposit successful"
        assert deposit_amount_resp.json()['data']['currency'] == deposit_data['currency']
        assert deposit_amount_resp.json()['data']['deposit_method'] == deposit_data['deposit_method']
        assert deposit_amount_resp.json()['data']['transaction_reference'] == deposit_data['transaction_reference']
        assert deposit_amount_resp.json()['data']['amount'] == deposit_data['amount']

        logger.info(f"Amount Deposited successfully with the following creds:\n{deposit_amount_resp.json()}")
