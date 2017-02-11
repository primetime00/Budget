import json
from datetime import date

class Budget:
    def __init__(self):
        self.budget = self.readBudget()
        self.income = self.readIncome()
        self.expenses = self.readExpenses()
        self.exclusions = self.readExclusions()
        self.credentials = self.readCredentials()

    def readFile(self, fname):
        data = {}
        with open(fname, "r") as fin:
            data = json.load(fin)
        return data

    def readExpenses(self):
        return self.readFile("expenses.json")

    def readBudget(self):
        return self.readFile("budget.json")

    def readIncome(self):
        return self.readFile("income.json")

    def readExclusions(self):
        return self.readFile("exclusions.json")

    def readCredentials(self):
        return self.readFile("credentials.json")

    def getExpenses(self):
        return self.expenses

    def getExclusions(self):
        return self.exclusions

    def getCredentials(self):
        return self.credentials

    def getCalculatedTotal(self):
        totalExpense = 0
        totalIncome = 0
        for expense in self.expenses:
            totalExpense += expense["amount"]
        td = date.today()
        if td.month == self.income["month"]:
            for income in self.income["income"]:
                totalIncome += income["amount"]
        totalBudget = self.budget["budget"]
        return totalBudget - totalExpense + totalIncome
