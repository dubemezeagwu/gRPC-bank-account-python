# Mock Distributed Banking System using gRPC and Redis

## Project Overview
This project implements a distributed banking system using gRPC for client-server communication and Redis for data persistence. The system allows for basic banking operations such as account creation, deposits, withdrawals, and interest calculations in a concurrent environment.

## Features
- Account creation (savings and checking accounts)
- Balance inquiries
- Deposit operations
- Withdrawal operations with insufficient funds protection
- Interest calculation and application
- Thread-safe operations using account-level locking
- Persistent storage using Redis
- Comprehensive error handling

## Technical Stack
- Python 3.x
- gRPC
- Protocol Buffers
- Redis (Latest)
- Docker (for Redis container)

## Prerequisites
- Python 3.x
- Docker
- pip package manager

## Project Structure
```
bank_grpc_project/
├── bank.proto             # Protocol Buffer service definitions
├── venv/                  # Python virtual environment
├── bank_pb2.py            # Generated Protocol Buffer code
├── bank_pb2_grpc.py       # Generated gRPC code
├── server.py              # gRPC server implementation
├── client.py              # gRPC client implementation
└── README.md              # This file
```

## Setup Instructions

1. Create and activate a Python virtual environment:
```bash
# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Unix/MacOS:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

2. Install required packages:
```bash
pip install grpcio grpcio-tools redis
```

3. Start Redis using Docker:
```bash
docker run -d -p 6379:6379 redis
```

4. Generate gRPC code from the protocol buffer definition:
```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bank.proto```

5. Start the server:
```bash
python server.py
```

6. In a separate terminal, run the client:
```bash
python client.py
```

## API Reference

### CreateAccount
Creates a new bank account.
- Parameters:
  - account_id (string): Unique identifier for the account
  - account_type (string): Either "savings" or "checking"
- Returns: Confirmation message

### GetBalance
Retrieves the current balance of an account.
- Parameters:
  - account_id (string): Account identifier
- Returns: Current balance

### Deposit
Adds funds to an account.
- Parameters:
  - account_id (string): Account identifier
  - amount (float): Amount to deposit
- Returns: Updated balance and confirmation message

### Withdraw
Removes funds from an account.
- Parameters:
  - account_id (string): Account identifier
  - amount (float): Amount to withdraw
- Returns: Updated balance and confirmation message

### CalculateInterest
Applies interest to the account balance.
- Parameters:
  - account_id (string): Account identifier
  - annual_interest_rate (float): Interest rate as a percentage
- Returns: Updated balance and confirmation message

## Error Handling
The system handles various error scenarios:
- Account not found
- Insufficient funds
- Invalid transaction amounts
- Invalid interest rates
- Invalid account types

## Concurrency
- Thread-safe operations using per-account locks
- Supports multiple simultaneous clients
- Prevents race conditions during balance updates

## Testing
You can test the system using the example code in the client's main function, which demonstrates:
1. Creating a new account
2. Making deposits
3. Checking balances
4. Making withdrawals
5. Calculating interest

## Future Improvements
Potential enhancements could include:
- Adding transaction history
- Implementing account transfer functionality
- Adding authentication and authorization
- Supporting different currencies
- Adding account statements generation
