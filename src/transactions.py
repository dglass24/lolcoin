class Transactions:
    def __init__(self):
        self.txns = []

    def add_transaction(self, txn):
        self.txns.append(txn)

    def get_transactions(self):
        return self.txns

    def clear_transactions(self):
        self.txns = []

transactions = Transactions()