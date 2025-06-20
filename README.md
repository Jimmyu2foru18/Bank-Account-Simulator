# Bank Account Simulator

## Overview
Python application demonstrating different banking implementations:
- **Stateful OOP implementation** with class-based account management and transaction history
- **Stateless functional implementation** using pure functions and immutable state

## Features
- GUI with tabbed interface
  - Account creation and management
  - Transaction operations
  - Transaction history viewer
  - Mode switching
- Command Line Interface (CLI)
- Runtime mode switching between implementations
- Transaction history in stateful mode
- Balance validation with overdraft protection

## Requirements
- Python 
- Tkinter (included with Python)

## Getting Started
```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

### GUI Mode (Default)
```bash
python main.py
```
or explicitly specify GUI mode:
```bash
python main.py --gui
```

### CLI Mode
```bash
python main.py --cli
```

### Stateful Mode Example
```python
account = BankAccount(100)
account.deposit(50)
print(account.get_balance())  
```

### Functional Mode Example
```python
balance = 100
balance = deposit(balance, 50)
print(get_balance(balance))
```

## Implementation Details
### OOP Approach (`BankAccount` class)
- Encapsulates balance state
- Maintains transaction history
- Methods modify internal state

### Functional Approach
- Pure functions: deposit → new_balance
- Immutable balance handling
- No side effects

## Tests
```bash
    pytest tests/
```

## Educational Value
    Demonstrates:
    - State management tradeoffs
    - Immutability vs encapsulation
    - Architectural flexibility patterns

## Design Decisions

| Aspect              | OOP Approach               | Functional Approach         |
|---------------------|---------------------------|------------------------------|
| State Management    | Encapsulated mutation     | Immutable returns            |
| Thread Safety       | Requires synchronization  | Naturally thread-safe        |
| Memory Usage        | Cumulative history        | Transient intermediate states|
| Debugging           | Instance inspection        | Function composition tracing |

## Extended Example (Stateful)
```python
account = BankAccount(500, overdraft_limit=1000)
account.withdraw(700) 
print(f"Current balance: {account.get_balance()}") 
print(f"Transaction count: {account.transaction_count()}")
```
