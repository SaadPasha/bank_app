import grpc
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

from bank_grpc import bank_pb2, bank_pb2_grpc
from bank_grpc.bank_server import BankService

app = FastAPI()

# gRPC server address
grpc_server_address = 'localhost:50052'
bank_service = BankService()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Generates custom validation error for the request body
    Args:
        request: Instance of the Request
        exc: Instance of the Validation class

    Returns: Validation error response
    """
    for error in exc.errors():
        error_msg = {
            "status": "failed",
            "error": {
                "message": f"Invalid parameter value: '{error['loc'][-1]}'",
                "details": error['msg']
            }
        }
        return JSONResponse(error_msg, status_code=400)


class CreateUserRequest(BaseModel):
    f_name: str = Field(..., min_length=2, max_length=255, pattern="[a-zA-Z]+")
    l_name: str = Field(..., min_length=2, max_length=255, pattern="[a-zA-Z]+")
    dob: str = Field(..., pattern="^\d{4}-\d{2}-\d{2}$")
    email: EmailStr = Field(..., min_length=8, max_length=50)
    address: str = Field(..., min_length=8, max_length=255, pattern="[a-zA-Z]+")
    phone: str = Field(..., min_length=6, max_length=20)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "f_name": "John",
                    "l_name": "Doe",
                    "dob": "1992-05-15",
                    "email": "john.doe@example.com",
                    "address": "123 Main Street",
                    "phone": "123-456-7890"
                }
            ]
        }
    }


class CreateUserResponse(BaseModel):
    status: str
    details: dict
    message: str
    generated_user_id: str
    initial_balance: float


@app.post("/create_user", response_model=CreateUserResponse)
async def create_user(user_data: CreateUserRequest):
    """
    Create a new user
    Args:
        user_data: The data of the user in JSON format

    Returns: User ID upon successful creation of user
    """
    try:
        # Call gRPC server to create a user
        with grpc.insecure_channel(grpc_server_address) as channel:
            stub = bank_pb2_grpc.BankServiceStub(channel)
            grpc_request = bank_pb2.CreateUserRequest(
                f_name=user_data.f_name,
                l_name=user_data.l_name,
                dob=user_data.dob,
                email=user_data.email,
                address=user_data.address,
                phone=user_data.phone
            )
            grpc_response = stub.CreateUser(grpc_request)

        # Convert gRPC response to a Python dictionary
        created_user = {
            "status": grpc_response.status,
            "details": {
                "message": grpc_response.details.message
            },
            "generated_user_id": grpc_response.generated_user_id,  # Include the generated user ID in the response
            "initial_balance": grpc_response.initial_balance
        }

        return JSONResponse(created_user, status_code=201)

    except grpc.RpcError as e:
        if "Duplicate Email or Phone number" in e.details():
            error_response = {
                "status": "failed",
                "error": {
                    "message": "Duplicate email address or phone",
                    "details": "The provided email address OR phone number is already associated with an existing account. Please use a different one."
                }
            }
            raise HTTPException(status_code=400, detail=error_response)

        else:
            # Handle gRPC errors
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


class DepositRequest(BaseModel):
    user_id: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]+$")
    amount: float = Field(..., gt=0, lt=100001)
    currency: str
    deposit_method: str
    transaction_reference: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "100001",
                    "amount": 2000,
                    "currency": "EUR",
                    "deposit_method": "cash_deposit",
                    "transaction_reference": "BANK123456789"
                }
            ]
        }
    }


class DepositResponse(BaseModel):
    status: str
    message: str
    data: dict


class DataDepositModel(BaseModel):
    currency: str
    deposit_method: str
    transaction_reference: str
    amount: float


@app.post("/deposit", response_model=DepositResponse)
async def deposit_amount(deposit_data: DepositRequest):
    """
    Deposit amount int a User's account
    Args:
        deposit_data: The data of the transaction in JSON format

    Returns: Transaction details upon successful deposit
    """
    try:
        # Call gRPC server to deposit amount
        with grpc.insecure_channel(grpc_server_address) as channel:
            stub = bank_pb2_grpc.BankServiceStub(channel)
            grpc_request = bank_pb2.DepositRequest(
                user_id=deposit_data.user_id,
                amount=deposit_data.amount,
                currency=deposit_data.currency,
                deposit_method=deposit_data.deposit_method,
                transaction_reference=deposit_data.transaction_reference
            )
            grpc_response = stub.DepositAmount(grpc_request)

            # Validate the currency
            if deposit_data.currency not in ["EUR", "USD"]:
                error_response = {
                    "status": "failed",
                    "error": {
                        "message": "Invalid currency",
                        "details": f"Deposits in '{deposit_data.currency}' are not allowed by the bank. Please use a supported currency such as USD or EUR."
                    }

                }
                raise HTTPException(status_code=400, detail=error_response)

            if deposit_data.deposit_method not in ["cash_deposit", "wire_transfer"]:
                error_response = {
                    "status": "failed",
                    "error": {
                        "message": "Invalid deposit method",
                        "details": f"The specified deposit method: '{deposit_data.deposit_method}' is not allowed by the bank. Please choose a valid deposit method."
                    }

                }
                raise HTTPException(status_code=400, detail=error_response)

        # Convert gRPC response to a Python dictionary
        deposited_amount = {
            "status": grpc_response.status,
            "message": grpc_response.message,
            "data": {
                "currency": grpc_response.data.currency,
                "deposit_method": grpc_response.data.deposit_method,
                "transaction_reference": grpc_response.data.transaction_reference,
                "amount": grpc_response.data.amount,
            },
        }
        return JSONResponse(deposited_amount, status_code=201)

    except grpc.RpcError as e:
        # Handle gRPC errors
        if "User not found" in e.details():
            error_response = {
                "status": "failed",
                "error": {
                    "message": "User not found",
                    "details": "The requested user with the provided ID does not exist. Please check the user ID and try again."
                }
            }
            raise HTTPException(status_code=404, detail=error_response)

        # Handle other gRPC errors
        else:
            # Handle gRPC errors
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


class GetBalanceResponse(BaseModel):
    status: str
    message: str
    data: dict


class DataBalanceModel(BaseModel):
    user_id : str
    amount : float
    currency: str

@app.get("/get_balance/{user_id}", response_model=GetBalanceResponse)
async def get_balance(user_id: str):
    """
    Get the current Balance of the User
    Args:
        user_id: The ID of the user

    Returns: Current Balance of the user

    """
    try:
        # Call gRPC server to get the balance
        with grpc.insecure_channel(grpc_server_address) as channel:
            stub = bank_pb2_grpc.BankServiceStub(channel)
            grpc_request = bank_pb2.GetBalanceRequest(user_id=user_id)
            grpc_response = stub.GetBalance(grpc_request)

        # Convert gRPC response to a Python dictionary
        current_balance = {
            "status": grpc_response.status,
            "message": grpc_response.message,
            "data": {
                "user_id": grpc_response.data.user_id,
                "balance": grpc_response.data.balance,
                "currency": grpc_response.data.currency,
            }
        }
        return current_balance

    except grpc.RpcError as e:
        # Handle gRPC errors
        if "User not found" in e.details():
            error_response = {
                "status": "failed",
                "error": {
                    "message": "User not found",
                    "details": "The requested user with the provided ID does not exist. Please check the user ID and try again."
                }
            }
            raise HTTPException(status_code=404, detail=error_response)
        else:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
