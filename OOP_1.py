from datetime import datetime, timedelta


# Base Class
class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"[{self.account_holder}] Deposited ${amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        print(f"[{self.account_holder}] Withdrew ${amount:.2f}")

    def get_balance(self):
        return self.balance

    def __str__(self):
        return (f"Account Number: {self.account_number}\n"
                f"Account Holder: {self.account_holder}\n"
                f"Balance: ${self.balance:.2f}")


# Subclass: SavingsAccount
class SavingsAccount(BankAccount):
    def __init__(self, account_number, account_holder, interest_rate, balance=0.0):
        super().__init__(account_number, account_holder, balance)
        self.interest_rate = interest_rate  # in percentage

    def apply_interest(self):
        interest = self.balance * (self.interest_rate / 100)
        self.balance += interest
        print(f"[{self.account_holder}] Interest applied: ${interest:.2f}")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}\nAccount Type: Savings\nInterest Rate: {self.interest_rate}%"


# Subclass: CurrentAccount
class CurrentAccount(BankAccount):
    def __init__(self, account_number, account_holder, overdraft_limit, balance=0.0):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Exceeds overdraft limit.")
        self.balance -= amount
        print(f"[{self.account_holder}] Withdrew ${amount:.2f} (Overdraft Allowed)")

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}\nAccount Type: Current\nOverdraft Limit: ${self.overdraft_limit:.2f}"


# Subclass: FixedDepositAccount
class FixedDepositAccount(BankAccount):
    def __init__(self, account_number, account_holder, lock_period_days, balance=0.0):
        super().__init__(account_number, account_holder, balance)
        self.lock_period_days = lock_period_days
        self.creation_date = datetime.now()

    def withdraw(self, amount):
        current_date = datetime.now()
        if current_date < self.creation_date + timedelta(days=self.lock_period_days):
            raise ValueError("Withdrawal not allowed before lock-in period ends.")
        super().withdraw(amount)

    def __str__(self):
        unlock_date = self.creation_date + timedelta(days=self.lock_period_days)
        base_str = super().__str__()
        return f"{base_str}\nAccount Type: Fixed Deposit\nUnlock Date: {unlock_date.date()}"


# Bank class to manage multiple accounts
class Bank:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account):
        if account.account_number in self.accounts:
            raise ValueError("Account with this number already exists.")
        self.accounts[account.account_number] = account

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    def transfer_funds(self, from_account_number, to_account_number, amount):
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)

        if not from_account or not to_account:
            raise ValueError("One or both accounts not found.")

        from_account.withdraw(amount)
        to_account.deposit(amount)
        print(f"Transferred ${amount:.2f} from {from_account.account_holder} to {to_account.account_holder}")


# ===========================
# ✅ Test Program / Demo
# ===========================

if __name__ == "__main__":
    # Create a bank
    my_bank = Bank()

    # Create accounts
    savings = SavingsAccount("S1001", "Alice", interest_rate=3.5, balance=1000)
    current = CurrentAccount("C1001", "Bob", overdraft_limit=500, balance=200)
    fixed = FixedDepositAccount("F1001", "Charlie", lock_period_days=30, balance=5000)

    # Add to bank
    my_bank.add_account(savings)
    my_bank.add_account(current)
    my_bank.add_account(fixed)

    # Perform operations
    print("\n--- Initial Account Info ---")
    print(savings)
    print(current)
    print(fixed)

    print("\n--- Savings Account Operations ---")
    savings.deposit(500)
    savings.apply_interest()
    savings.withdraw(200)

    print("\n--- Current Account Operations ---")
    current.withdraw(600)  # Uses overdraft
    current.deposit(300)

    print("\n--- Attempt Early Withdrawal from Fixed Deposit ---")
    try:
        fixed.withdraw(1000)
    except ValueError as e:
        print("Error:", e)

    print("\n--- Transfer Funds from Savings to Current ---")
    my_bank.transfer_funds("S1001", "C1001", 300)

    print("\n--- Final Balances ---")
    print(savings)
    print(current)
    print(fixed)
