class DepositParams(object):
    def __init__(self, user_id=None, amount=1000.0, currency="EUR",
                 deposit_method="cash_deposit", transaction_reference="BANK123456789"):
        self.user_id = user_id
        self.amount = amount
        self.currency = currency
        self.deposit_method = deposit_method
        self.transaction_reference = transaction_reference


    def gen_deposit_data(self) -> dict:
        deposit_data = {
            "user_id": self.user_id,
            "amount": self.amount,
            "currency": self.currency,
            "deposit_method": self.deposit_method,
            "transaction_reference": self.transaction_reference
        }
        return deposit_data
