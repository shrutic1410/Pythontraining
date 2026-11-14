import unittest

class InsufficientFundsError(Exception):
    """Custom exception raised when a withdrawal violates the minimum balance limit."""
    pass


class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        self.balance -= amount
        return self.balance

    # Bonus Challenge: Beautifully formatted string representation
    def __str__(self):
        return f"[Account Holder: {self.owner} | Available Balance: {self.balance}]"


class SavingsAccount(Account):
    def __init__(self, owner, balance, min_balance=500):
        # Reusing the parent constructor via super()
        super().__init__(owner, balance)
        self.min_balance = min_balance

    # Overriding the withdraw method to enforce rules
    def withdraw(self, amount):
        if self.balance - amount < self.min_balance:
            raise InsufficientFundsError(
                f"Error: Insufficient funds; balance {self.balance}, requested {amount}"
            )
        super().withdraw(amount)
        return f"{self.owner} withdrew {amount} -> balance {self.balance}"


# --- Automated Testing Suite ---

class TestSavingsAccount(unittest.TestCase):
    
    def setUp(self):
        """Runs before every test to give us a fresh test subject."""
        self.priya = SavingsAccount("Priya", 1500)

    def test_failed_withdrawal(self):
        """Verifies that withdrawing below minimum balance raises InsufficientFundsError."""
        with self.assertRaises(InsufficientFundsError):
            self.priya.withdraw(1200)

    def test_successful_withdrawal(self):
        """Verifies that a valid withdrawal updates the balance correctly."""
        result = self.priya.withdraw(800)
        self.assertEqual(self.priya.balance, 700)
        self.assertEqual(result, "Priya withdrew 800 -> balance 700")

    def test_deposit(self):
        """Verifies that deposits successfully increase the balance."""
        self.priya.deposit(300)
        self.assertEqual(self.priya.balance, 1800)

    def test_inheritance_isinstance(self):
        """Verifies subclass inheritance relationship."""
        self.assertTrue(isinstance(self.priya, Account))

    def test_string_representation(self):
        """Verifies the custom __str__ formatting output."""
        self.assertEqual(str(self.priya), "[Account Holder: Priya | Available Balance: 1500]")


# --- Run Tests and Original Verification Script ---
if __name__ == "__main__":
    print("--- Running Original Requirement Logs ---")
    
    # 1. Re-running the precise scenario requested in the prompt
    priya_demo = SavingsAccount("Priya", 1500)
    
    # Try 1200
    try:
        priya_demo.withdraw(1200)
    except InsufficientFundsError as e:
        print(e)
        
    # Try 800
    try:
        print(priya_demo.withdraw(800))
    except InsufficientFundsError as e:
        print(e)
        
    # isinstance explanation printout
    print(isinstance(priya_demo, Account))
    
    # String representation challenge demo
    print(f"Bonus __str__ output: {priya_demo}\n")