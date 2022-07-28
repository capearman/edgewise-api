
class Metrics:
    def __init__(self, actual_income: float, planned_income: float, actual_expenses: float, planned_expenses: float, last_month_balance: float):
        self.actual_income = actual_income
        self.planned_income = planned_income
        self.actual_expenses = actual_expenses
        self.planned_expenses = planned_expenses
        self.last_month_balance = last_month_balance
        self.money_to_categorize = last_month_balance + actual_income - planned_expenses
        self.current_balance = planned_expenses - actual_expenses

    def get_money_to_categorize(self):
        return self.money_to_categorize

    def get_current_balance(self):
        return self.current_balance

class MetricsOut:
    def __init__(self) -> None:
        pass
    
    