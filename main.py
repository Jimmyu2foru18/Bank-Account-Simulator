"""Bank Account Simulator Main Entry Point

This serves as the main entry point for the Bank Account Simulator,
allowing users to choose between the CLI and GUI interfaces.
"""

import sys
import argparse


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Bank Account Simulator")
    parser.add_argument(
        "--cli", 
        action="store_true", 
        help="Run the command-line interface version"
    )
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Run the graphical user interface version (default)"
    )
    
    args = parser.parse_args()

    if not args.cli and not args.gui:
        args.gui = True
    
    if args.cli:
        from src.app import BankAccountSimulator
        simulator = BankAccountSimulator()
        simulator.run()
    else:
        import tkinter as tk
        from src.gui import BankAccountSimulatorGUI
        root = tk.Tk()
        app = BankAccountSimulatorGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()