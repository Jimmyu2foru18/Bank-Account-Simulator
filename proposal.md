# Bank Account Simulator Project Proposal

## Objective
Demonstrate banking operations through dual implementations:
- Stateful OOP approach with encapsulation
- Stateless functional approach with immutability

## Technical Approach
1. **Core Implementations**
   - `BankAccount` class with balance state and transaction history
   - Pure functions: `deposit()`, `withdraw()`, `get_balance()`
2. **UI System**
   - Text-based menu using `input()`/`print()`
   - Runtime mode switching capability
3. **Key Differentiators**
   - Live implementation swapping without restart
   - Transaction audit trail in stateful version

## Educational Value
- Contrasts OOP encapsulation vs functional purity
- Demonstrates state management tradeoffs
- Shows implementation flexibility patterns

## Project Structure
```
/src
  bank_account.py  # Both implementations
  app.py           # CLI interface
/tests
  test_operations.py
```

## Architecture Diagrams
```mermaid
flowchart TD
    CLI[Text Interface] -->|Stateful Mode| OOP[BankAccount Class]
    CLI -->|Functional Mode| FP[Pure Functions]
    OOP -->|Maintains| State[Balance + History]
    FP -->|Returns| NewState[Immutable Balance]
    
## Learning Objectives
- Compare mutation vs immutability patterns
- Analyze memory implications of state approaches
- Evaluate thread safety considerations
