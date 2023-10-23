class Category:

    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = []

    def __str__(self):
        category_display = self.category_name.center(30, "*") + "\n"
        for entry in self.ledger:
            formatted_description = f"{entry['description'][:23]:23}"
            formatted_amount = f"{entry['amount']:7.2f}"
            category_display += formatted_description + formatted_amount + "\n"
        category_display += "Total: " + str(self.get_balance())
        return category_display

    def deposit(self, amount, description=""):
        transaction = {}
        transaction['amount'] = amount
        transaction['description'] = description
        self.ledger.append(transaction)

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            transaction = {}
            transaction['amount'] = -amount
            transaction['description'] = description
            self.ledger.append(transaction)
            return True
        return False

    def get_balance(self):
        balance = 0
        for entry in self.ledger:
            balance += entry['amount']
        return balance

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + other_category.category_name)
            other_category.deposit(amount, "Transfer from " + self.category_name)
            return True
        return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

def create_spend_chart(categories):
    spending = []
    for category in categories:
        total_spent = 0
        for entry in category.ledger:
            if entry['amount'] < 0:
                total_spent += abs(entry['amount'])
        spending.append(total_spent)

    total_spending = sum(spending)
    spending_percentage = [spend / total_spending * 100 for spend in spending]

    chart = "Percentage spent by category"
    for i in range(100, -1, -10):
        chart += "\n" + str(i).rjust(3) + "|"
        for percentage in spending_percentage:
            if percentage > i:
                chart += " o "
            else:
                chart += "   "
        chart += " "

    chart += "\n    ----------"

    category_name_lengths = [len(category.category_name) for category in categories]
    max_name_length = max(category_name_lengths)

    for i in range(max_name_length):
        chart += "\n    "
        for category in categories:
            if i < len(category.category_name):
                chart += " " + category.category_name[i] + " "
            else:
                chart += "   "
        chart += " "

    return chart
