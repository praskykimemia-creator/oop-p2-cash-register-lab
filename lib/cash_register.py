#!/usr/bin/env python3

#!/usr/bin/env python3

class CashRegister:
    """
    Models a cash register: tracks a running total, the items currently
    added, and a log of transactions so the last one can be voided.
    """

    def __init__(self, discount=0):
        # Goes through the discount setter so validation runs on init too.
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        """
        Discount is a whole-number percentage (0-100 inclusive) taken off
        the register's total, e.g. discount = 20 means 20% off.
        """
        # Excluding bool explicitly since True/False are technically ints.
        is_valid = isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 100

        if is_valid:
            self._discount = value
        else:
            print("Not valid discount")
            self._discount = getattr(self, "_discount", 0)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def add_item(self, item, price, quantity=1):
        """
        Add an item to the register: increases total by price * quantity,
        appends the item name once per unit purchased, and logs the
        transaction so it can be voided later.
        """
        self.total += price * quantity
        self.items.extend([item] * quantity)
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity,
        })

    def apply_discount(self):
        """
        Apply the register's discount percentage to the current total.
        Prints an error message instead if there's nothing in the cart
        or if there's no discount set.
        """
        if not self.previous_transactions or not self.discount:
            print("There is no discount to apply.")
            return

        self.total -= self.total * (self.discount / 100)
        print(f"After the discount, the total comes to ${self.total:g}.")

    def void_last_transaction(self):
        """
        Remove the most recently added transaction: subtracts its
        price * quantity back out of the total and removes that many
        copies of the item from self.items.
        """
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        last_transaction = self.previous_transactions.pop()
        quantity = last_transaction["quantity"]
        self.total -= last_transaction["price"] * quantity

        if quantity > 0:
            # The last `quantity` entries in items are exactly the ones added
            # by this transaction, since add_item appends them contiguously.
            del self.items[-quantity:]
