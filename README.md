bank_app - gRPC, FastAPI, Pytest
===========================================================
This project contains the Hybrid demo banking application (Backend only) developed using gRPC and FastAPI. The Automated API tests are developed using using Pytest and Requests.

Project Structure
-----------------
```
.
├── Dockerfile
├── __init__.py
├── api_tests
│   ├── Dockerfile
│   ├── api_data
│   │   ├── deposit_params.py
│   │   └── user_params.py
│   ├── api_helpers.py
│   ├── req_setup.py
│   ├── tests
│   │   ├── conftest.py
│   │   ├── create_user
│   │   │   ├── test_create_new_user.py
│   │   │   ├── test_create_user_invalid_payload.py
│   │   │   ├── test_create_user_missing_fields.py
│   │   │   └── test_invalid_boundary_val_check.py
│   │   ├── deposit
│   │   │   ├── test_deposit_invalid_amount.py
│   │   │   ├── test_deposit_invalid_user_id.py
│   │   │   └── test_deposit_succes.py
│   │   ├── get_balance
│   │   │   ├── test_get_balance_invalid_user.py
│   │   │   └── test_get_balance_success.py
│   └── user_api_utils.py
├── bank_grpc
│   ├── Dockerfile
│   ├── __init__.py
│   ├── bank_pb2.py
│   ├── bank_pb2_grpc.py
│   ├── bank_server.py
│   └── protos
│       ├── __init__.py
│       └── bank.proto
├── base_config.json
├── base_script.py
├── docker-compose.yml
├── logger.py
├── logs
├── main.py
├── pytest.ini
└── requirements.txt

```


### App
The application works in a way that the gRPC server handles the main logic (CRUD Operations) and the FastAPI server communicates to it as a Client, whereas the Fast API endpoints are exposed to the end users which are used to send Requests using JSON.
The goal is to mimic the microservice architecture in the real world, where the internal operational speed is increased by as the gRPC requests being binary data, are handled in a faster and quicker manner.

The REST endpoints are:
/create_user: Create a new user
/deposit: Deposit amount int a User's account
/get_balance: Get the current Balance of the User

Each of this API endpoint communicate with the gRPC Server functions to perform its operations.
You can run Fastapi locally and check the documentation as:
1. Navigate to the /bank_app/
2. Run the command ```uvicorn main:app --host 127.0.0.1 --port 8000 --reload```
3. Open Browser and goto: http://127.0.0.1:8000/docs

### Tests
The automated test suites are developed using Pytest with AllureReports 2.0 and Request library package.
The tests are designed using the ['Layered Architecture'](https://medium.com/@iamsanjeevkumar/test-automation-framework-with-layered-architecture-968f2dfbd3cb).
Which in a nutshell is to separate the test scripts, the test logic, and the test data. For this project, if you check the
/bank_app/, you will find the following files and dirs:

- /api_tests/
  - req_setup.py: HTTP requests configuration
  - user_api_utils.py: Functions to make redundant API calls
  - api_helpers.py: Small functions to generate runtime data
  - api_data/ The data structures for each API endpoint
  - tests/ Test scripts root 
  - tests/conftest.py: Fixtures to inject data structures and configurations
- /base_config.json and base_script.py: To load the configuration for each environment
- /logger.py: The customized logger

Using, test are very much isolated and independent and therefore, less flaky.
For example, if a change is required in the request payload, it can solely be done in the api_data/{endpoint}_params.py file 
and this will update all the other tests scripts. Another example could be that if the 'headers' require change, then you only
need to update the 'base_config.json' file and that's it!

Also, the solution is fully dockerized, therefore, CI/CD deployment can be done easily.

Requirements
------------
1. Linux or WSL setup would be great, although Windows can work but I am not sure about Paths.
2. Python 3.10+
3. Docker

Technical Setup & Execution
---------------
1. Clone the repo in your system.

Execution
---------------
1. After installing docker, navigate to current working dir to the: **bank_app/**
2. Run the following command: 
   -  `docker-compose build`: This will build 6 docker images for the test suites - allure, allure-ui, api-tests, grpc-serve and fastapi-server.  All dependencies will be installed automatically.
3. Next, Run the following command to spin up the images:
   - `docker-compose up` - This will start all the four containers.
4. Wait for a few seconds for the tests to finish.
5. Lastly, open the following link in your local browser:
    - [Allure Test Reports](http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html?redirect=false)

Troubleshoot
------------
I do hope there aren't any problems, but just incase:
- If there's HTTP connection timeout in the test output, please try to run tests manually.
  - For manual execution, first update the following file(s):
    - bank_app/base_config.json (Update from ```api_host_config.api_web_host: fastapi-server:8000``` to  ```api_host_config.api_web_host: 127.0.0.1:8000```
    - bank_app/main.py (Update line 14 from ```grpc_server_address = 'grpc-server:50052'``` to ```grpc_server_address = 'localhost:50052'```
  - Next, open three terminal windows, and run the following commands in each one:
    - ```python bank_grpc/bank_server.py``` Should run the gRPC server
    - ```uvicorn main:app --host 127.0.0.1 --port 8000 --reload``` Should run the FastAPI server
    - ```python -m pytest api_tests/tests/``` Should run the API tests

NB!! Please make sure that the PYTHONPATH for the current directory is up-to-date.

### References:
- https://pytest-html.readthedocs.io/en/latest/
- https://requests.readthedocs.io/en/latest/
- https://docs.docker.com/reference/
- https://github.com/fescobar/allure-docker-service-ui
- https://grpc.io/docs/languages/python/quickstart
- https://fastapi.tiangolo.com/
- 

### Contact: 
In case of any issues, please feel free to contact me at: saadtahir96@outlook.com