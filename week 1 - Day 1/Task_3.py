# Create the custom exception InsufficientFundsError
class InsufficientFundsError(Exception):
    pass

# Create the Account class
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"{self.owner} deposited {amount} -> balance {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            # Raise the custom exception with a descriptive message
            raise InsufficientFundsError(f"Insufficient funds: balance {self.balance}, requested {amount}")
        self.balance -= amount
        print(f"{self.owner} withdrew {amount} -> balance {self.balance}")

    def show(self):
        print(f"Account Owner: {self.owner}, Balance: {self.balance}")

# Test the implementation using try/except/finally
if __name__ == "__main__":
    # Create Arun with an initial balance of 1000
    arun_account = Account("Arun", 1000)
    
    try:
        # Deposit 500
        arun_account.deposit(500)
        # Try to withdraw 2000 (which will trigger the exception)
        arun_account.withdraw(2000)
        
    except InsufficientFundsError as e:
        # Catch and print the error message
        print(f"Error: {e}")
        
    finally:
        # Ensure this block always executes
        print("Transaction finished")