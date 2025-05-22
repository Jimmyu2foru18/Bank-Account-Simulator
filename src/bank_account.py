"""Bank Account Simulator
"""
from typing import Dict, List, Tuple, Union, Optional
from datetime import datetime

class BankAccount:
    """A stateful bank account implementation using OOP.
    
    Attributes:
        _balance: Account balance
        _transaction_history: All transactions
        _overdraft_limit: Maximum allowed negative balance
    """
    
    def __init__(self, initial_balance: float = 0, overdraft_limit: float = 0):
        """Initialize a new bank account.
        
        Args:
            initial_balance: Starting balance for the account
            overdraft_limit: Maximum allowed negative balance
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self._balance = initial_balance
        self._transaction_history = []
        self._overdraft_limit = max(0, overdraft_limit)  

        if initial_balance > 0:
            self._record_transaction("initial deposit", initial_balance)
    
    def deposit(self, amount: float) -> float:
        """Deposit money into the account.
        
        Args:
            amount: Amount to deposit
            
        Returns:
            The new balance
            
        Raises:
            ValueError: If amount is negative or zero
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self._balance += amount
        self._record_transaction("deposit", amount)
        return self._balance
    
    def withdraw(self, amount: float) -> float:
        """Withdraw money from the account.
        
        Args:
            amount: Amount to withdraw
            
        Returns:
            The new balance
            
        Raises:
            ValueError: If amount is negative or zero
            ValueError: If withdrawal would exceed overdraft limit
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if self._balance - amount < -self._overdraft_limit:
            raise ValueError(f"Withdrawal would exceed overdraft limit of {self._overdraft_limit}")
        
        self._balance -= amount
        self._record_transaction("withdrawal", amount)
        return self._balance
    
    def get_balance(self) -> float:
        """Get the current account balance.
        
        Returns:
            The current balance
        """
        return self._balance
    
    def get_transaction_history(self) -> List[Dict]:
        """Get the transaction history.
        
        Returns:
            A list of transaction records
        """
        return self._transaction_history.copy()
    
    def transaction_count(self) -> int:
        """Get the number of transactions performed.
        
        Returns:
            The number of transactions
        """
        return len(self._transaction_history)
    
    def _record_transaction(self, transaction_type: str, amount: float) -> None:
        """Record a transaction in the history.
        
        Args:
            transaction_type: Type of transaction
            amount: Amount involved in the transaction
        """
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "timestamp": datetime.now(),
            "resulting_balance": self._balance
        }
        self._transaction_history.append(transaction)

def deposit(balance: float, amount: float) -> float:
    """Deposit money and return new balance.
    
    Args:
        balance: Current balance
        amount: Amount to deposit
        
    Returns:
        New balance after deposit
        
    Raises:
        ValueError: If amount is negative or zero
    """
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")
    
    return balance + amount


def withdraw(balance: float, amount: float, overdraft_limit: float = 0) -> float:
    """Withdraw money and return new balance.
    
    Args:
        balance: Current balance
        amount: Amount to withdraw
        overdraft_limit: Maximum allowed negative balance
        
    Returns:
        New balance after withdrawal
        
    Raises:
        ValueError: If amount is negative or zero
        ValueError: If withdrawal would exceed overdraft limit
    """
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    
    new_balance = balance - amount
    if new_balance < -overdraft_limit:
        raise ValueError(f"Withdrawal would exceed overdraft limit of {overdraft_limit}")
    
    return new_balance


def get_balance(balance: float) -> float:
    """Get the current balance.
    
    Args:
        balance: Current balance
        
    Returns:
        The current balance
    """
    return balance