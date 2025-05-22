"""Tests for Bank Account Simulator

This module contains tests for both the stateful (OOP) and
stateless (functional) implementations of the bank account.
"""

import sys
import os
import unittest
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.bank_account import BankAccount, deposit, withdraw, get_balance


class TestStatefulBankAccount(unittest.TestCase):
    """Tests for the stateful OOP."""
    
    def setUp(self):
        """Set up a fresh bank account before each test."""
        self.account = BankAccount(100, 200) 
    
    def test_initial_balance(self):
        """Test that the initial balance is set correctly."""
        self.assertEqual(self.account.get_balance(), 100)
    
    def test_deposit(self):
        """Test deposit functionality."""
        new_balance = self.account.deposit(50)
        self.assertEqual(new_balance, 150)
        self.assertEqual(self.account.get_balance(), 150)
    
    def test_withdraw(self):
        """Test withdrawal functionality."""
        new_balance = self.account.withdraw(30)
        self.assertEqual(new_balance, 70)
        self.assertEqual(self.account.get_balance(), 70)
    
    def test_overdraft_allowed(self):
        """Test that withdrawals within overdraft limit are allowed."""
        new_balance = self.account.withdraw(250) 
        self.assertEqual(new_balance, -150)
    
    def test_overdraft_exceeded(self):
        """Test that exceeding overdraft limit raises an error."""
        with self.assertRaises(ValueError):
            self.account.withdraw(350) 
    
    def test_negative_deposit(self):
        """Test that negative deposits are rejected."""
        with self.assertRaises(ValueError):
            self.account.deposit(-50)
    
    def test_negative_withdrawal(self):
        """Test that negative withdrawals are rejected."""
        with self.assertRaises(ValueError):
            self.account.withdraw(-50)
    
    def test_transaction_history(self):
        """Test that transaction history is recorded correctly."""
        self.account.deposit(50)
        self.account.withdraw(30)
        
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["type"], "initial deposit")
        self.assertEqual(history[1]["type"], "deposit")
        self.assertEqual(history[2]["type"], "withdrawal")
        
        self.assertEqual(history[0]["amount"], 100)
        self.assertEqual(history[1]["amount"], 50)
        self.assertEqual(history[2]["amount"], 30)
        
        self.assertEqual(history[2]["resulting_balance"], 120)
    
    def test_transaction_count(self):
        """Test the transaction count method."""
        self.account.deposit(50)
        self.account.withdraw(30)
        
        self.assertEqual(self.account.transaction_count(), 3)


class TestStatelessBankAccount(unittest.TestCase):
    """Tests for the stateless functional implementation."""
    
    def setUp(self):
        """Set up the initial balance before each test."""
        self.balance = 100
        self.overdraft_limit = 200
    
    def test_deposit(self):
        """Test deposit functionality."""
        new_balance = deposit(self.balance, 50)
        self.assertEqual(new_balance, 150)
        self.assertEqual(self.balance, 100)
    
    def test_withdraw(self):
        """Test withdrawal functionality."""
        new_balance = withdraw(self.balance, 30, self.overdraft_limit)
        self.assertEqual(new_balance, 70)
        self.assertEqual(self.balance, 100)
    
    def test_overdraft_allowed(self):
        """Test that withdrawals within overdraft limit are allowed."""
        new_balance = withdraw(self.balance, 250, self.overdraft_limit) 
        self.assertEqual(new_balance, -150)
    
    def test_overdraft_exceeded(self):
        """Test that exceeding overdraft limit raises an error."""
        with self.assertRaises(ValueError):
            withdraw(self.balance, 350, self.overdraft_limit)
    
    def test_negative_deposit(self):
        """Test that negative deposits are rejected."""
        with self.assertRaises(ValueError):
            deposit(self.balance, -50)
    
    def test_negative_withdrawal(self):
        """Test that negative withdrawals are rejected."""
        with self.assertRaises(ValueError):
            withdraw(self.balance, -50, self.overdraft_limit)
    
    def test_get_balance(self):
        """Test the get_balance function."""
        result = get_balance(self.balance)
        self.assertEqual(result, self.balance)


if __name__ == "__main__":
    unittest.main()