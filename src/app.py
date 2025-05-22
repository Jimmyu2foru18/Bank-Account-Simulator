"""Bank Account Simulator Application

This module provides a command-line interface for interacting with
both the stateful (OOP) and stateless (functional) bank account implementations.
"""

import sys
from typing import Dict, List, Callable, Any, Optional
from src.bank_account import BankAccount, deposit, withdraw, get_balance


class BankAccountSimulator:
    """Command-line interface for the Bank Account Simulator.
    
    This class manages the interaction between the user and the
    different bank account implementations.
    """
    
    def __init__(self):
        """Initialize the simulator with both implementations."""
        # Mode flags
        self.current_mode = "stateful" 
        self.account = None
        self.balance = 0
        self.overdraft_limit = 0
        
        # Menu options
        self.menu_options = {
            "1": self.create_account,
            "2": self.make_deposit,
            "3": self.make_withdrawal,
            "4": self.check_balance,
            "5": self.view_transaction_history,
            "6": self.switch_mode,
            "7": self.exit_program
        }
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n===== Bank Account Simulator =====")
        print(f"Current Mode: {'OOP (Stateful)' if self.current_mode == 'stateful' else 'Functional (Stateless)'}")
        
        if self.current_mode == 'stateful':
            balance = self.account.get_balance() if self.account else 0
        else:
            balance = self.balance
            
        print(f"Current Balance: ${balance:.2f}")
        print("\nOptions:")
        print("1. Create new account")
        print("2. Make a deposit")
        print("3. Make a withdrawal")
        print("4. Check balance")
        print("5. View transaction history (Stateful mode only)")
        print("6. Switch mode (Stateful/Functional)")
        print("7. Exit")
    
    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to the Bank Account Simulator!")
        print("This application demonstrates two different implementation approaches:")
        print("  - Stateful (Object-Oriented Programming)")
        print("  - Stateless (Functional Programming)")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-7): ")
            
            action = self.menu_options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")
    
    def create_account(self) -> None:
        """Create a new bank account."""
        try:
            initial_balance = float(input("Enter initial balance: $"))
            overdraft_limit = float(input("Enter overdraft limit (0 for none): $"))
            
            if self.current_mode == 'stateful':
                self.account = BankAccount(initial_balance, overdraft_limit)
                print(f"Account created with balance: ${initial_balance:.2f}")
            else:
                self.balance = initial_balance
                self.overdraft_limit = overdraft_limit
                print(f"Account created with balance: ${self.balance:.2f}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def make_deposit(self) -> None:
        """Make a deposit to the account."""
        if self._check_account_exists():
            try:
                amount = float(input("Enter deposit amount: $"))
                
                if self.current_mode == 'stateful':
                    new_balance = self.account.deposit(amount)
                else:
                    self.balance = deposit(self.balance, amount)
                    new_balance = self.balance
                    
                print(f"Deposit successful. New balance: ${new_balance:.2f}")
            except ValueError as e:
                print(f"Error: {e}")
    
    def make_withdrawal(self) -> None:
        """Make a withdrawal from the account."""
        if self._check_account_exists():
            try:
                amount = float(input("Enter withdrawal amount: $"))
                
                if self.current_mode == 'stateful':
                    new_balance = self.account.withdraw(amount)
                else:
                    self.balance = withdraw(self.balance, amount, self.overdraft_limit)
                    new_balance = self.balance
                    
                print(f"Withdrawal successful. New balance: ${new_balance:.2f}")
            except ValueError as e:
                print(f"Error: {e}")
    
    def check_balance(self) -> None:
        """Check the current account balance."""
        if self._check_account_exists():
            if self.current_mode == 'stateful':
                balance = self.account.get_balance()
            else:
                balance = get_balance(self.balance)
                
            print(f"Current balance: ${balance:.2f}")
    
    def view_transaction_history(self) -> None:
        """View the transaction history (stateful mode only)."""
        if self.current_mode != 'stateful':
            print("Transaction history is only available in stateful (OOP) mode.")
            return
            
        if self._check_account_exists():
            history = self.account.get_transaction_history()
            
            if not history:
                print("No transactions recorded yet.")
                return
                
            print("\n===== Transaction History =====")
            for i, transaction in enumerate(history, 1):
                print(f"Transaction #{i}:")
                print(f"  Type: {transaction['type']}")
                print(f"  Amount: ${transaction['amount']:.2f}")
                print(f"  Date: {transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Resulting Balance: ${transaction['resulting_balance']:.2f}")
                print()
                
            print(f"Total transactions: {len(history)}")
    
    def switch_mode(self) -> None:
        """Switch between stateful and stateless modes."""
        if self.current_mode == 'stateful':
            if self.account:
                self.balance = self.account.get_balance()
            self.current_mode = 'stateless'
            print("Switched to Functional (Stateless) mode.")
        else:
            self.account = BankAccount(self.balance, self.overdraft_limit)
            self.current_mode = 'stateful'
            print("Switched to OOP (Stateful) mode.")
    
    def exit_program(self) -> None:
        """Exit the program."""
        print("Thank you for using the Bank Account Simulator!")
        sys.exit(0)
    
    def _check_account_exists(self) -> bool:
        """Check if an account has been created.
        
        Returns:
            True if account exists, False otherwise
        """
        if self.current_mode == 'stateful' and not self.account:
            print("Please create an account first (Option 1).")
            return False
        return True


if __name__ == "__main__":
    simulator = BankAccountSimulator()
    simulator.run()