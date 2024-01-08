from api_tests import user_api_utils
import allure


@allure.title("Balance - BE - Retrieve balance successfully")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("The test case verifies that in case a GET request is sent to the endpoint: /get_balance - with the valid user ID specified in the request headers "
                    "- the system is able to process the data and return the current balance of the user.")
def test_retrieve_balance_success(config, deposit_data, user_data, get_balance_url,
                                  create_user_url, deposit_amount_url, logger):
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
    new_user_id = user_api_utils.create_new_user(url=create_user_url, data=user_data, headers=config.headers).json()['generated_user_id']
    print(new_user_id)
    with allure.step("With new user, Send a GET request with the user ID specified in the query_param."):
        get_balance_url = get_balance_url + "/" + new_user_id
        get_balance_resp = user_api_utils.get_balance(url=get_balance_url, headers=config.headers)

        assert get_balance_resp.status_code == 200
        assert get_balance_resp.json()['status'] == "success"
        assert get_balance_resp.json()['message'] == "User balance retrieved successfully"
        assert get_balance_resp.json()['data']['user_id'] == new_user_id
        assert get_balance_resp.json()['data']['balance'] == 0.0

        logger.info(f"Initial Balance retrieved with response JSON:\n{get_balance_resp.json()}")

    with allure.step("Send a POST request to the /deposit endpoint, in order to add amount."):
        deposit_data['user_id'] = new_user_id
        deposit_data['amount'] = 1000
        deposit_amount_resp = user_api_utils.deposit_amount(url=deposit_amount_url, data=deposit_data, headers=config.headers)
        assert deposit_amount_resp.status_code == 201

        logger.info(f"Amount added successfully with response JSON:\n{deposit_amount_resp.json()}")

    with allure.step("Send a GET request again with the same user ID specified in the query_param."):
        get_balance_resp = user_api_utils.get_balance(url=get_balance_url, headers=config.headers)
        assert get_balance_resp.status_code == 200
        assert get_balance_resp.json()['status'] == "success"
        assert get_balance_resp.json()['message'] == "User balance retrieved successfully"
        assert get_balance_resp.json()['data']['user_id'] == new_user_id
        assert get_balance_resp.json()['data']['balance'] == 1000.0
