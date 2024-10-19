
import random
import string
from datetime import date
from typing import Dict, Any
# from "@interledger/openai" import HttpMethod, Response Validator
print("Hello, world")

# Mocking the TypeScript imports and functions
class OutgoingPaymentRoutes:
    def create(self, requestArgs: Dict[str, Any], createArgs: Dict[str, Any]) -> Dict[str, Any]:
        # This is a mock implementation
        print(f"Creating outgoing payment: {createArgs}")
        return {"id": "payment_123", "status": "completed"}


def createOutgoingPaymentRoutes(deps: Dict[str, Any]) -> OutgoingPaymentRoutes:
    return OutgoingPaymentRoutes()


# Voucher system
class MoneyVoucher:
    def __init__(self, sender, recipient, amount, message):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.message = message
        self.voucher_code = self.generate_voucher_code()
        self.issue_date = date.today().strftime("%m/%d/%Y")
        self.redeemed = False

    def generate_voucher_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def print_voucher(self):
        return f"""
        ================================
        MONEY VOUCHER
        ================================
        Voucher Code: {self.voucher_code}
        Date: {self.issue_date}

        To: {self.recipient}
        From: {self.sender}
        Amount: ${self.amount:.2f}

        Message: {self.message}

        ================================
        This voucher is redeemable ONCE for the amount stated above.
        ================================
        """

    def redeem(self):
        if not self.redeemed:
            self.redeemed = True
            return self.amount
        return None


# Dictionary to store created vouchers
vouchers = {}


# Mock Interledger client
class InterledgerClient:
    def __init__(self):
        self.payment_routes = createOutgoingPaymentRoutes({})

    def make_payment(self, sender: str, recipient: str, amount: float) -> bool:
        payment_args = {
            "amount": str(int(amount * 100)),  # Convert to cents
            "assetCode": "USD",
            "assetScale": 2,
            "receiver": recipient
        }
        try:
            result = self.payment_routes.create({}, payment_args)
            return result["status"] == "completed"
        except Exception as e:
            print(f"Payment failed: {str(e)}")
            return False


interledger_client = InterledgerClient()


def create_voucher():
    sender = input("Enter your wallet ID: ")
    recipient = input("Enter the recipient's wallet ID: ")

    while True:
        amount_str = input("Enter the amount to send: ")
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be positive. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    message = input("Enter a personal message: ")

    # Create the voucher
    voucher = MoneyVoucher(sender, recipient, amount, message)
    vouchers[voucher.voucher_code] = voucher

    # Attempt to make the payment using Interledger
    if interledger_client.make_payment(sender, recipient, amount):
        print("Payment successful! Here's your voucher:")
        print(voucher.print_voucher())
    else:
        print("Payment failed. Voucher creation cancelled.")
        del vouchers[voucher.voucher_code]


def check_voucher():
    code = input("Enter the voucher code: ")
    if code in vouchers:
        voucher = vouchers[code]
        if not voucher.redeemed:
            print(f"Valid voucher found!")
            print(f"Recipient: {voucher.recipient}")
            print(f"Amount: ${voucher.amount:.2f}")
            print(f"Message: {voucher.message}")

            redeem = input("Do you want to redeem this voucher now? (yes/no): ").lower()
            if redeem == 'yes':
                amount = voucher.redeem()
                if amount is not None:
                    print(f"Voucher successfully redeemed! You have received ${amount:.2f}")
                    print("This voucher cannot be used again.")
                else:
                    print("Error: Voucher has already been redeemed.")
            else:
                print("Voucher not redeemed. You can redeem it later.")
        else:
            print("This voucher has already been redeemed and cannot be used again.")
    else:
        print("Invalid voucher code. Please check and try again.")


def main_menu():
    while True:
        print("\n===== Money Voucher System with Interledger =====")
        print("1. Create a new voucher")
        print("2. Check/Redeem a voucher")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            create_voucher()
        elif choice == '2':
            check_voucher()
        elif choice == '3':
            print("Thank you for using the Money Voucher System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()