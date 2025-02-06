import grpc
import bank_pb2
import bank_pb2_grpc

class BankClient:
    def __init__(self, host='localhost', port=50051):
        # Create a channel to the server
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        # Create a stub (client)
        self.stub = bank_pb2_grpc.BankServiceStub(self.channel)

    def create_account(self, account_id: str, account_type: str) -> str:
        """Creates a new account"""
        request = bank_pb2.AccountRequest(
            account_id=account_id,
            account_type=account_type
        )
        try:
            response = self.stub.CreateAccount(request)
            return response.message
        except grpc.RpcError as e:
            return f"Error: {e.details()}"

    def get_balance(self, account_id: str) -> float:
        """Retrieves the balance for the specified account"""
        request = bank_pb2.AccountRequest(account_id=account_id)
        try:
            response = self.stub.GetBalance(request)
            return response.balance
        except grpc.RpcError as e:
            print(f"Error: {e.details()}")
            return -1

    def deposit(self, account_id: str, amount: float) -> str:
        """Deposits the given amount into the specified account"""
        request = bank_pb2.DepositRequest(
            account_id=account_id,
            amount=amount
        )
        try:
            response = self.stub.Deposit(request)
            return response.message
        except grpc.RpcError as e:
            return f"Error: {e.details()}"

    def withdraw(self, account_id: str, amount: float) -> str:
        """Withdraws the given amount from the specified account"""
        request = bank_pb2.WithdrawRequest(
            account_id=account_id,
            amount=amount
        )
        try:
            response = self.stub.Withdraw(request)
            return response.message
        except grpc.RpcError as e:
            return f"Error: {e.details()}"

    def calculate_interest(self, account_id: str, annual_interest_rate: float) -> str:
        """Applies the specified annual interest rate to the account balance"""
        request = bank_pb2.InterestRequest(
            account_id=account_id,
            annual_interest_rate=annual_interest_rate
        )
        try:
            response = self.stub.CalculateInterest(request)
            return response.message
        except grpc.RpcError as e:
            return f"Error: {e.details()}"

def main():
    # Create a client instance
    client = BankClient()

    # Example usage
    print("Creating new account...")
    print(client.create_account("1234", "savings"))

    print("\nDepositing money...")
    print(client.deposit("1234", 1000.0))

    print("\nChecking balance...")
    balance = client.get_balance("1234")
    print(f"Current balance: ${balance:.2f}")

    print("\nWithdrawing money...")
    print(client.withdraw("1234", 500.0))

    print("\nCalculating interest...")
    print(client.calculate_interest("1234", 2.5))

    print("\nFinal balance...")
    balance = client.get_balance("1234")
    print(f"Final balance: ${balance:.2f}")

# def main():
#     # Create a client instance
#     client = BankClient()

#     # Example usage
#     print("Creating new account...")
#     print(client.create_account("5678", "savings"))

#     print("\nDepositing money...")
#     print(client.deposit("5678", 1000.0))

#     print("\nChecking balance...")
#     balance = client.get_balance("5678")
#     print(f"Current balance: ${balance:.2f}")

#     print("\nWithdrawing money...")
#     print(client.withdraw("5678", 500.0))

#     print("\nCalculating interest...")
#     print(client.calculate_interest("5678", 2.5))

#     print("\nFinal balance...")
#     balance = client.get_balance("5678")
#     print(f"Final balance: ${balance:.2f}")

if __name__ == '__main__':
    main()