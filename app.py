"""Bank Account Simulator

Main entry point for the Bank Account Simulator application.
This file simply imports and runs the simulator from the src package.
"""

from src.app import BankAccountSimulator

if __name__ == "__main__":
    simulator = BankAccountSimulator()
    simulator.run()