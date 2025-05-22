"""Bank Account Simulator GUI

This GUI is for interacting with both the stateful "OOP" and 
stateless "("functional" bank account implementations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
from src.bank_account import BankAccount, deposit, withdraw, get_balance


class BankAccountSimulatorGUI:
    """GUI

    This class manages the interaction between the user and the
    different bank account states.
    """
    
    def __init__(self, root):
        """Initialize the simulator.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Bank Account Simulator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.current_mode = "stateful"
        self.account = None
        self.balance = 0
        self.overdraft_limit = 0
        self._create_ui()
        self._show_welcome_message()
    
    def _create_ui(self):
        """Create the main user interface."""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="Bank Account Simulator", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        self.mode_var = tk.StringVar(value="OOP (Stateful)")
        ttk.Label(header_frame, text="Mode: ").pack(side=tk.RIGHT)
        self.mode_label = ttk.Label(header_frame, textvariable=self.mode_var, font=("Arial", 10, "italic"))
        self.mode_label.pack(side=tk.RIGHT, padx=(0, 10))

        balance_frame = ttk.Frame(self.main_frame)
        balance_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(balance_frame, text="Current Balance: ", font=("Arial", 12)).pack(side=tk.LEFT)
        self.balance_var = tk.StringVar(value="$0.00")
        ttk.Label(balance_frame, textvariable=self.balance_var, font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.account_tab = ttk.Frame(self.notebook, padding=10)
        self.transaction_tab = ttk.Frame(self.notebook, padding=10)
        self.history_tab = ttk.Frame(self.notebook, padding=10)
        self.settings_tab = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.account_tab, text="Account")
        self.notebook.add(self.transaction_tab, text="Transactions")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.settings_tab, text="Settings")

        self._setup_account_tab()
        self._setup_transaction_tab()
        self._setup_history_tab()
        self._setup_settings_tab()

        self.status_var = tk.StringVar()
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        self.status_var.set("Ready. Please create an account to begin.")
    
    def _setup_account_tab(self):
        """Setup the account creation."""
        ttk.Label(self.account_tab, text="Create New Account", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(self.account_tab, text="Initial Balance:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.initial_balance_var = tk.StringVar()
        ttk.Entry(self.account_tab, textvariable=self.initial_balance_var).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(self.account_tab, text="Overdraft Limit:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.overdraft_limit_var = tk.StringVar()
        ttk.Entry(self.account_tab, textvariable=self.overdraft_limit_var).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Button(self.account_tab, text="Create Account", command=self._create_account).grid(row=3, column=0, columnspan=2, pady=10)
        info_frame = ttk.LabelFrame(self.account_tab, text="Account Information", padding=10)
        info_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Label(info_frame, text="Account Status:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.account_status_var = tk.StringVar(value="No account created")
        ttk.Label(info_frame, textvariable=self.account_status_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Current Balance:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.account_balance_var = tk.StringVar(value="$0.00")
        ttk.Label(info_frame, textvariable=self.account_balance_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="Overdraft Limit:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.account_overdraft_var = tk.StringVar(value="$0.00")
        ttk.Label(info_frame, textvariable=self.account_overdraft_var).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Make the columns expandable
        self.account_tab.columnconfigure(1, weight=1)
    
    def _setup_transaction_tab(self):
        """Setup the transaction tab for deposits and withdrawals."""
        ttk.Label(self.transaction_tab, text="Account Transactions", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        deposit_frame = ttk.LabelFrame(self.transaction_tab, text="Make a Deposit", padding=10)
        deposit_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, 5), pady=5)
        
        ttk.Label(deposit_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.deposit_amount_var = tk.StringVar()
        ttk.Entry(deposit_frame, textvariable=self.deposit_amount_var).grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        ttk.Button(deposit_frame, text="Deposit", command=self._make_deposit).grid(row=1, column=0, columnspan=2, pady=5)
        withdrawal_frame = ttk.LabelFrame(self.transaction_tab, text="Make a Withdrawal", padding=10)
        withdrawal_frame.grid(row=1, column=1, sticky=tk.NSEW, padx=(5, 0), pady=5)
        
        ttk.Label(withdrawal_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.withdrawal_amount_var = tk.StringVar()
        ttk.Entry(withdrawal_frame, textvariable=self.withdrawal_amount_var).grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        ttk.Button(withdrawal_frame, text="Withdraw", command=self._make_withdrawal).grid(row=1, column=0, columnspan=2, pady=5)
        quick_frame = ttk.LabelFrame(self.transaction_tab, text="Quick Actions", padding=10)
        quick_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        ttk.Button(quick_frame, text="Check Balance", command=self._check_balance).pack(side=tk.LEFT, padx=5)
        self.transaction_tab.columnconfigure(0, weight=1)
        self.transaction_tab.columnconfigure(1, weight=1)
        self.transaction_tab.rowconfigure(1, weight=1)
        deposit_frame.columnconfigure(1, weight=1)
        withdrawal_frame.columnconfigure(1, weight=1)
    
    def _setup_history_tab(self):
        """Setup the transaction history tab."""
        ttk.Label(self.history_tab, text="Transaction History", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(0, 10))
        self.history_info_var = tk.StringVar(value="Transaction history is only available in stateful (OOP) mode.")
        ttk.Label(self.history_tab, textvariable=self.history_info_var).pack(anchor=tk.W, pady=(0, 5))
        history_frame = ttk.Frame(self.history_tab)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, height=15)
        self.history_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.history_text.config(state=tk.DISABLED)
        ttk.Button(self.history_tab, text="Refresh History", command=self._refresh_history).pack(anchor=tk.W)
    
    def _setup_settings_tab(self):
        """Setup the settings tab for mode switching."""
        ttk.Label(self.settings_tab, text="Application Settings", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        mode_frame = ttk.LabelFrame(self.settings_tab, text="Implementation Mode", padding=10)
        mode_frame.grid(row=1, column=0, sticky=tk.NSEW, pady=5)
        
        self.mode_selection = tk.StringVar(value="stateful")
        ttk.Radiobutton(mode_frame, text="OOP (Stateful)", variable=self.mode_selection, value="stateful").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="Functional (Stateless)", variable=self.mode_selection, value="stateless").pack(anchor=tk.W, pady=2)
        
        ttk.Button(mode_frame, text="Apply Mode Change", command=self._switch_mode).pack(pady=10)
        about_frame = ttk.LabelFrame(self.settings_tab, text="About", padding=10)
        about_frame.grid(row=2, column=0, sticky=tk.NSEW, pady=5)
        
        about_text = """Bank Account Simulator demonstrates two programming paradigms:
        
1. Object-Oriented Programming
   - Uses a BankAccount class to maintain state
   - Tracks transaction history
   - Encapsulates data and behavior

2. Functional Programming
   - Uses pure functions without side effects
   - State is passed explicitly as parameters
   - No transaction history
"""
        
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.LEFT, wraplength=400)
        about_label.pack(fill=tk.BOTH, expand=True)
        ttk.Button(self.settings_tab, text="Exit Application", command=self._exit_program).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.settings_tab.columnconfigure(0, weight=1)
    
    def _show_welcome_message(self):
        """Display a welcome message when the application starts."""
        welcome_text = """Welcome to the Bank Account Simulator!

This application was created to demonstrate two different implementations:
- Stateful 
- Stateless 

To get started, create a new account in the Account tab."""
        
        messagebox.showinfo("Welcome", welcome_text)
    
    def _create_account(self):
        """Create a new bank account."""
        try:
            initial_balance_str = self.initial_balance_var.get().strip()
            overdraft_limit_str = self.overdraft_limit_var.get().strip()
            try:
                initial_balance = float(initial_balance_str) if initial_balance_str else 0.0
            except ValueError:
                raise ValueError("Initial balance must be a valid number")
                
            try:
                overdraft_limit = float(overdraft_limit_str) if overdraft_limit_str else 0.0
            except ValueError:
                raise ValueError("Overdraft limit must be a valid number")
            
            # Validate values
            if initial_balance < 0:
                raise ValueError("Initial balance cannot be negative")
            if overdraft_limit < 0:
                raise ValueError("Overdraft limit cannot be negative")

            if self.current_mode == 'stateful':
                self.account = BankAccount(initial_balance, overdraft_limit)
            else:
                self.balance = initial_balance
                self.overdraft_limit = overdraft_limit

            self._update_balance_display()
            self.account_status_var.set("Account active")
            self.account_balance_var.set(f"${initial_balance:.2f}")
            self.account_overdraft_var.set(f"${overdraft_limit:.2f}")
            self.balance_var.set(f"${initial_balance:.2f}")
            self.initial_balance_var.set("")
            self.overdraft_limit_var.set("")

            self.status_var.set(f"Account created with balance: ${initial_balance:.2f}")
            self.notebook.select(1)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _make_deposit(self):
        """Make a deposit to the account."""
        if not self._check_account_exists():
            return
            
        try:
            amount = float(self.deposit_amount_var.get() or 0)
            
            if self.current_mode == 'stateful':
                new_balance = self.account.deposit(amount)
            else:
                self.balance = deposit(self.balance, amount)
                new_balance = self.balance
            
            # Update UI
            self._update_balance_display()
            self.deposit_amount_var.set("")
            self.status_var.set(f"Deposit successful. New balance: ${new_balance:.2f}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _make_withdrawal(self):
        """Make a withdrawal from the account."""
        if not self._check_account_exists():
            return
            
        try:
            amount = float(self.withdrawal_amount_var.get() or 0)
            
            if self.current_mode == 'stateful':
                new_balance = self.account.withdraw(amount)
            else:
                self.balance = withdraw(self.balance, amount, self.overdraft_limit)
                new_balance = self.balance

            self._update_balance_display()
            self.withdrawal_amount_var.set("")
            self.status_var.set(f"Withdrawal successful. New balance: ${new_balance:.2f}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _check_balance(self):
        """Check and display the current account balance."""
        if not self._check_account_exists():
            return
            
        if self.current_mode == 'stateful':
            balance = self.account.get_balance()
        else:
            balance = get_balance(self.balance)
        
        messagebox.showinfo("Balance", f"Current balance: ${balance:.2f}")
        self.status_var.set(f"Balance checked: ${balance:.2f}")
    
    def _refresh_history(self):
        """Refresh and display the transaction history."""
        if self.current_mode != 'stateful':
            self.history_info_var.set("Transaction history is only available in stateful (OOP) mode.")
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, "Switch to OOP (Stateful) mode to view transaction history.")
            self.history_text.config(state=tk.DISABLED)
            return
            
        if not self._check_account_exists():
            return
            
        history = self.account.get_transaction_history()
        
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not history:
            self.history_text.insert(tk.END, "No transactions recorded yet.")
        else:
            self.history_info_var.set(f"Total transactions: {len(history)}")
            
            for i, transaction in enumerate(history, 1):
                self.history_text.insert(tk.END, f"Transaction #{i}:\n")
                self.history_text.insert(tk.END, f"  Type: {transaction['type']}\n")
                self.history_text.insert(tk.END, f"  Amount: ${transaction['amount']:.2f}\n")
                self.history_text.insert(tk.END, f"  Date: {transaction['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                self.history_text.insert(tk.END, f"  Resulting Balance: ${transaction['resulting_balance']:.2f}\n\n")
        
        self.history_text.config(state=tk.DISABLED)
        self.status_var.set("Transaction history refreshed.")
    
    def _switch_mode(self):
        """Switch between stateful and stateless modes."""
        new_mode = self.mode_selection.get()
        
        if new_mode == self.current_mode:
            self.status_var.set(f"Already in {new_mode} mode.")
            return

        if self._check_account_exists(show_message=False):
            if self.current_mode == 'stateful' and new_mode == 'stateless':
                self.balance = self.account.get_balance()
                self.mode_var.set("Functional (Stateless)")
                self.status_var.set("Switched to Functional (Stateless) mode.")
            elif self.current_mode == 'stateless' and new_mode == 'stateful':
                self.account = BankAccount(self.balance, self.overdraft_limit)
                self.mode_var.set("OOP (Stateful)")
                self.status_var.set("Switched to OOP (Stateful) mode.")
        else:
            self.mode_var.set("Functional (Stateless)" if new_mode == 'stateless' else "OOP (Stateful)")
            self.status_var.set(f"Switched to {new_mode} mode. No account exists yet.")
        
        self.current_mode = new_mode
        self._update_balance_display()
        
        if self.current_mode == 'stateless':
            self.history_info_var.set("Transaction history is only available in stateful (OOP) mode.")
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, "Switch to OOP (Stateful) mode to view transaction history.")
            self.history_text.config(state=tk.DISABLED)
    
    def _update_balance_display(self):
        """Update the balance display in the UI."""
        if self.current_mode == 'stateful' and self.account:
            balance = self.account.get_balance()
        elif self.current_mode == 'stateless':
            balance = self.balance
        else:
            balance = 0
            
        self.balance_var.set(f"${balance:.2f}")
        self.account_balance_var.set(f"${balance:.2f}")
    
    def _check_account_exists(self, show_message=True):
        """Check if an account has been created.
        
        Args:
            show_message: Whether to show an error message if no account exists
            
        Returns:
            True if account exists, False otherwise
        """
        if (self.current_mode == 'stateful' and not self.account) or \
           (self.current_mode == 'stateless' and self.account_status_var.get() != "Account active"):
            if show_message:
                messagebox.showwarning("No Account", "Please create an account first in the Account tab.")
                self.notebook.select(0) 
            return False
        return True
    
    def _exit_program(self):
        """Exit the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.root.destroy()


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = BankAccountSimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()