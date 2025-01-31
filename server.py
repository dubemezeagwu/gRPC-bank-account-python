import grpc
from concurrent import futures
import redis
import time
from threading import Lock

import bank_pb2
import bank_pb2_grpc

class BankServiceServicer(bank_pb2_grpc.BankServiceServicer):
    def __init__(self):
        # Initialize Redis connection
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        # Dictionary to store locks for each account
        self.account_locks = {}
        # Lock for creating new account locks
        self.lock_creation_lock = Lock()

    def get_account_lock(self, account_id):
        """Get or create a lock for an account"""
        with self.lock_creation_lock:
            if account_id not in self.account_locks:
                self.account_locks[account_id] = Lock()
            return self.account_locks[account_id]

    def CreateAccount(self, request, context):
        # Validate account type
        if request.account_type not in ['savings', 'checking']:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Account type must be 'savings' or 'checking'")
            return bank_pb2.AccountResponse()

        # Check if account already exists
        if self.redis_client.exists(request.account_id):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Account already exists")
            return bank_pb2.AccountResponse()

        # Create account in Redis
        account_data = {
            'account_type': request.account_type,
            'balance': 0.0
        }
        self.redis_client.hset(request.account_id, account_data)

        return bank_pb2.AccountResponse(
            account_id=request.account_id,
            message=f"Account {request.account_id} created successfully"
        )

    def GetBalance(self, request, context):
        # Check if account exists
        if not self.redis_client.exists(request.account_id):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Account not found. Please check the account ID.")
            return bank_pb2.BalanceResponse()

        # Get balance from Redis
        balance = float(self.redis_client.hget(request.account_id, 'balance'))
        
        return bank_pb2.BalanceResponse(
            account_id=request.account_id,
            balance=balance,
            message="Balance retrieved successfully"
        )

    def Deposit(self, request, context):
        # Validate amount
        if request.amount <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Transaction amount must be positive.")
            return bank_pb2.TransactionResponse()

        # Get lock for this account
        with self.get_account_lock(request.account_id):
            # Check if account exists
            if not self.redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found. Please check the account ID.")
                return bank_pb2.TransactionResponse()

            # Update balance in Redis
            current_balance = float(self.redis_client.hget(request.account_id, 'balance'))
            new_balance = current_balance + request.amount
            self.redis_client.hset(request.account_id, 'balance', new_balance)

            return bank_pb2.TransactionResponse(
                account_id=request.account_id,
                message=f"Successfully deposited ${request.amount:.2f}",
                balance=new_balance
            )

    def Withdraw(self, request, context):
        # Validate amount
        if request.amount <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Transaction amount must be positive.")
            return bank_pb2.TransactionResponse()

        # Get lock for this account
        with self.get_account_lock(request.account_id):
            # Check if account exists
            if not self.redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found. Please check the account ID.")
                return bank_pb2.TransactionResponse()

            # Check sufficient funds
            current_balance = float(self.redis_client.hget(request.account_id, 'balance'))
            if current_balance < request.amount:
                context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                context.set_details("Insufficient funds for the requested withdrawal.")
                return bank_pb2.TransactionResponse()

            # Update balance in Redis
            new_balance = current_balance - request.amount
            self.redis_client.hset(request.account_id, 'balance', new_balance)

            return bank_pb2.TransactionResponse(
                account_id=request.account_id,
                message=f"Successfully withdrew ${request.amount:.2f}",
                balance=new_balance
            )

    def CalculateInterest(self, request, context):
        # Validate interest rate
        if request.annual_interest_rate <= 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Annual interest rate must be a positive value.")
            return bank_pb2.TransactionResponse()

        # Get lock for this account
        with self.get_account_lock(request.account_id):
            # Check if account exists
            if not self.redis_client.exists(request.account_id):
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found. Please check the account ID.")
                return bank_pb2.TransactionResponse()

            # Calculate interest
            current_balance = float(self.redis_client.hget(request.account_id, 'balance'))
            interest = current_balance * (request.annual_interest_rate / 100)
            new_balance = current_balance + interest
            self.redis_client.hset(request.account_id, 'balance', new_balance)

            return bank_pb2.TransactionResponse(
                account_id=request.account_id,
                message=f"Successfully applied {request.annual_interest_rate}% interest",
                balance=new_balance
            )

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add the service to the server
    bank_pb2_grpc.add_BankServiceServicer_to_server(
        BankServiceServicer(), server)
    
    # Listen on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    
    print("Server started on port 50051")
    
    try:
        while True:
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()