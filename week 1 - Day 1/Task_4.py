class InsufficientFundsError(Exception):
    """Custom exception raised when the withdrawal goes below the minimum balance."""
    pass


class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        self.balance -= amount

    # Bonus Challenge: Adding __str__ method to Account
    def __str__(self):
        return f"Owner: {self.owner}, Balance: {self.balance}"


class SavingsAccount(Account):
    def __init__(self, owner, balance, min_balance=500):
        # Use super().__init__() to reuse the parent constructor
        super().__init__(owner, balance)
        self.min_balance = min_balance

    # Override withdraw to enforce the minimum balance rule
    def withdraw(self, amount):
        if self.balance - amount < self.min_balance:
            raise InsufficientFundsError(
                f"Error: Insufficient funds; balance {self.balance}, requested {amount}"
            )
        super().withdraw(amount)
        print(f"{self.owner} withdrew {amount} -> balance {self.balance}")


# --- Execution and Verification ---

# Create Priya with a starting balance of 1500
priya = SavingsAccount("Priya", 1500)

# Try to withdraw 1200 (Will fail: 1500 - 1200 = 300, which is below min_balance 500)
try:
    priya.withdraw(1200)
except InsufficientFundsError as e:
    print(e)

# Try to withdraw 800 (Will succeed: 1500 - 800 = 700, which is >= 500)
try:
    priya.withdraw(800)
except InsufficientFundsError as e:
    print(e)

# Print isinstance verification
is_instance_check = isinstance(priya, Account)
print(is_instance_check)
