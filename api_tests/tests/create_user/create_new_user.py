from api_tests import user_api_utils
import allure
import sys
sys.path.append('/')

@allure.title("Create new User - Valid Credentials")
def test_create_new_user(config, user_data, create_user_url, logger):
    print(user_data)
    create_user = user_api_utils.create_new_user(url=create_user_url, data=user_data, headers=config.headers)

    assert create_user.status_code == 201
    logger.info(f"User created successfully with the following creds:\n{create_user.json()}")
