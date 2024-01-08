from concurrent import futures

import grpc
import bank_pb2, bank_pb2_grpc


class BankService(bank_pb2_grpc.BankServiceServicer):

    def __init__(self):
        self.users = {}  # Dictionary to store user information with user_id as the key
        self.user_id_counter = 100000  # Counter for generating unique user_id


    def CreateUser(self, request, context):
        self.user_id_counter += 1
        user_id = str(self.user_id_counter)

        for user_data in self.users.values():
            if user_data['email'] == request.email or user_data['phone'] == request.phone:
                context.set_details("Duplicate Email or Phone number")
                return bank_pb2.CreateUserResponse(message="Duplicate Email or Phone number")

        # Add the user to the internal memory
        self.users[user_id] = {
            "f_name": request.f_name,
            "l_name": request.l_name,
            "dob": request.dob,
            "email": request.email,
            "address": request.address,
            "phone": request.phone,
            "balance": 0
        }

        print(self.users)

        response = bank_pb2.CreateUserResponse(
            status="success",
            details=bank_pb2.CreateUserResponse.Details(
                message="A new user account has been created successfully"
            ),
            generated_user_id=user_id,  # Include the generated user ID in the response
            initial_balance=0
        )

        return response

    def DepositAmount(self, request, context):
        user_id = request.user_id
        amount = request.amount
        currency = request.currency
        deposit_method = request.deposit_method
        transaction_reference = request.transaction_reference

        # Check if the user exists
        if user_id not in self.users:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return bank_pb2.DepositResponse(status="failure", message="User not found")

        # Update the user's balance
        self.users[user_id]["balance"] += amount

        print(self.users[user_id]["balance"])

        response = bank_pb2.DepositResponse(
            status="success",
            message="Deposit successful",
            data=bank_pb2.DepositResponse.Data(
                currency=currency,
                deposit_method=deposit_method,
                transaction_reference=transaction_reference,
                amount=amount,
            ),
        )
        return response

    def GetBalance(self, request, context):
        user_id = request.user_id

        # Check if the user exists
        if user_id not in self.users:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return bank_pb2.GetBalanceResponse(status="failure", message="User not found")

        # Retrieve the user's balance
        current_balance = self.users[user_id]["balance"]

        response = bank_pb2.GetBalanceResponse(
            status="success",
            message="User balance retrieved successfully",
            data=bank_pb2.GetBalanceResponse.Data(
                user_id=user_id,
                balance=current_balance,
                currency="EUR"
            ),
        )
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    bank_pb2_grpc.add_BankServiceServicer_to_server(BankService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC server running")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
