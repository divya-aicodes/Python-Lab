"""Model and operate a bank account using object-oriented programming."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def normalize_money(value: Decimal | str | int) -> Decimal:
    """Return a finite monetary value rounded to two decimal places."""
    amount = Decimal(value)
    if not amount.is_finite():
        raise ValueError("Amount must be finite.")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Transaction:
    """Represent one account transaction."""

    transaction_type: str
    amount: Decimal
    balance_after: Decimal


class BankAccount:
    """Represent a bank account with controlled balance updates."""

    def __init__(
        self, account_number: str, holder_name: str, opening_balance: Decimal = Decimal("0")
    ) -> None:
        if not account_number.strip() or not holder_name.strip():
            raise ValueError("Account number and holder name are required.")
        balance = normalize_money(opening_balance)
        if balance < 0:
            raise ValueError("Opening balance cannot be negative.")

        self._account_number = account_number.strip()
        self._holder_name = holder_name.strip()
        self._balance = balance
        self._transactions: list[Transaction] = []
        if balance:
            self._record("OPENING BALANCE", balance)

    @property
    def account_number(self) -> str:
        """Return the account number."""
        return self._account_number

    @property
    def holder_name(self) -> str:
        """Return the account holder's name."""
        return self._holder_name

    @property
    def balance(self) -> Decimal:
        """Return the current balance."""
        return self._balance

    @property
    def transactions(self) -> tuple[Transaction, ...]:
        """Return an immutable view of transaction history."""
        return tuple(self._transactions)

    def _record(self, transaction_type: str, amount: Decimal) -> None:
        self._transactions.append(Transaction(transaction_type, amount, self._balance))

    def deposit(self, amount: Decimal | str | int) -> Decimal:
        """Deposit a positive amount and return the new balance."""
        normalized_amount = normalize_money(amount)
        if normalized_amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self._balance += normalized_amount
        self._record("DEPOSIT", normalized_amount)
        return self._balance

    def withdraw(self, amount: Decimal | str | int) -> Decimal:
        """Withdraw an available positive amount and return the new balance."""
        normalized_amount = normalize_money(amount)
        if normalized_amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        if normalized_amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= normalized_amount
        self._record("WITHDRAWAL", normalized_amount)
        return self._balance

    def display_details(self) -> None:
        """Display account information."""
        print(f"Account Number : {self.account_number}")
        print(f"Holder Name    : {self.holder_name}")
        print(f"Balance        : {self.balance:.2f}")

    def display_transactions(self) -> None:
        """Display transaction history."""
        if not self.transactions:
            print("No transactions are available.")
            return
        print(f"{'Type':<20} {'Amount':>12} {'Balance':>12}")
        print("-" * 46)
        for transaction in self.transactions:
            print(
                f"{transaction.transaction_type:<20} {transaction.amount:>12.2f} "
                f"{transaction.balance_after:>12.2f}"
            )


def read_amount(prompt: str, allow_zero: bool = False) -> Decimal:
    """Read a valid monetary amount."""
    while True:
        try:
            amount = normalize_money(input(prompt).strip())
        except (InvalidOperation, ValueError):
            print("Enter a valid finite amount.")
            continue
        if amount > 0 or (allow_zero and amount == 0):
            return amount
        print("Amount must be positive.")


def main() -> None:
    """Create an account and run its operations menu."""
    print("========== BANK ACCOUNT SYSTEM ==========")
    account_number = input("Enter account number: ").strip()
    holder_name = input("Enter account holder name: ").strip()
    opening_balance = read_amount("Enter opening balance: ", allow_zero=True)
    try:
        account = BankAccount(account_number, holder_name, opening_balance)
    except ValueError as error:
        print(f"Unable to create account: {error}")
        return

    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Display account details")
        print("4. Display transaction history")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                balance = account.deposit(read_amount("Enter deposit amount: "))
                print(f"Deposit successful. Balance: {balance:.2f}")
            elif choice == "2":
                balance = account.withdraw(read_amount("Enter withdrawal amount: "))
                print(f"Withdrawal successful. Balance: {balance:.2f}")
            elif choice == "3":
                account.display_details()
            elif choice == "4":
                account.display_transactions()
            elif choice == "5":
                print("Bank account system closed.")
                break
            else:
                print("Invalid choice. Enter a number from 1 to 5.")
        except ValueError as error:
            print(f"Transaction failed: {error}")


if __name__ == "__main__":
    main()
