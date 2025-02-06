import threading
import time
from client import BankClient

def perform_transactions(client, account_id, transactions):
    """Perform a series of transactions and print results"""
    for transaction_type, amount in transactions:
        if transaction_type == "deposit":
            result = client.deposit(account_id, amount)
        else:  # withdraw
            result = client.withdraw(account_id, amount)
        print(f"Account {account_id}: {transaction_type} ${amount}: {result}")
        balance = client.get_balance(account_id)
        print(f"Account {account_id} balance: ${balance}")

def test_concurrent_access():
    # Create two clients
    client1 = BankClient()
    client2 = BankClient()

    # Create test accounts
    client1.create_account("test1", "checking")
    client1.create_account("test2", "checking")

    # Define transactions for each client
    client1_transactions = [
        ("deposit", 100),
        ("withdraw", 30),
        ("deposit", 50)
    ]

    client2_transactions = [
        ("deposit", 200),
        ("withdraw", 80),
        ("deposit", 40)
    ]

    # Create threads for concurrent access
    # Same account test
    print("\nTesting concurrent access to the same account:")
    thread1 = threading.Thread(
        target=perform_transactions,
        args=(client1, "test1", client1_transactions)
    )
    thread2 = threading.Thread(
        target=perform_transactions,
        args=(client2, "test1", client2_transactions)
    )

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads to complete
    thread1.join()
    thread2.join()

    # Different accounts test
    print("\nTesting concurrent access to different accounts:")
    thread3 = threading.Thread(
        target=perform_transactions,
        args=(client1, "test1", client1_transactions)
    )
    thread4 = threading.Thread(
        target=perform_transactions,
        args=(client2, "test2", client2_transactions)
    )

    # Start threads
    thread3.start()
    thread4.start()

    # Wait for threads to complete
    thread3.join()
    thread4.join()

if __name__ == "__main__":
    test_concurrent_access()