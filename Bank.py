from plaid import Client
from plaid import errors as plaid_errors
import json

class Bank:
    def __init__(self, credentials, gte):
        self.credentials = credentials
        self.bank = ""
        self.login = ""
        self.password = ""
        self.gte = gte
        self.accountName = ""
        self.expenses = None
        self.exclusions = None
        self.debug = False

    def requestTransactions(self):
        if "token" not in self.credentials["plaid"]:
            client = Client(client_id=self.credentials["plaid"]["client"], secret=self.credentials["plaid"]["secret"])
            data = ""
            try:
                response = client.connect(self.bank, {
                    'username': self.login,
                    'password': self.password
                })
                data = response.json()
            except plaid_errors.UnauthorizedError as e:
                print("AHHH")
                print(e.message)
                exit()
            token = data['access_token']
            self.credentials["plaid"]["token"] = token


        client = Client(client_id=self.credentials["plaid"]["client"], secret=self.credentials["plaid"]["secret"], access_token=self.credentials["plaid"]["token"])
        if self.debug == True:
            options = {'pending': True, 'gte': '2017/01/01'}
        else:
            options = {'pending': True, 'gte': self.gte}
        response = client.connect_get(opts=options)
        self.data = response.json()


    def processTransactions(self):
        accounts = self.data['accounts']
        transactions = self.data['transactions']
        id = self.getMainId(accounts)
        self.transactions = self.filterTransactions(id, transactions)
        if self.debug == True:
            from pprint import pprint
            with open(self.bank+".log", "w") as fin:
                for trans in self.transactions:
                    fin.write('{}, "{}", {}\n'.format(trans["date"], trans["name"], trans["amount"]))




    def getMainId(self, accounts):
        for account in accounts:
            name = account["meta"]["name"]
            if self.accountName in name:
                return account["_id"]


    def filterTransactions(self, id, trans):
        res = []
        for val in trans:
            if val["_account"] == id:
                res.append(val)
        return res

    def getKeys(self, data):
        keyList = []
        for item in data:
            keyList.append(item["name"])
        return keyList


    def getAmount(self, transaction, expenseNames):
        print(transaction["name"] + ", " + str(transaction["amount"]))
        for expenseName in expenseNames:
            if expenseName.lower() in transaction["name"].lower():
                print("------Excluding transaction (expense) {}".format(transaction["name"]))
                return 0
        return transaction["amount"]

    def getExpenseAndExclusions(self):
        expenses = self.expenses
        exclusions = self.exclusions
        expenseNames = []
        if expenses != None:
            expenseNames += self.getKeys(expenses)
        if exclusions != None:
            expenseNames += self.exclusions
        return expenseNames


    def getSpending(self):
        totalAmount = 0
        expenseNames = self.getExpenseAndExclusions()
        for trans in self.transactions:
            totalAmount += self.getAmount(trans, expenseNames)
        return totalAmount

    def setExclusions(self, exclusions):
        self.exclusions = exclusions

    def setExpenses(self, expenses):
        self.expenses = expenses

    def getLoginInfo(self):
        for bank in self.credentials["banks"]:
            if bank["name"] == self.bank:
                return (bank["user"], bank["pass"])
        raise Exception("Cannot find bank!")

    def getCredentials(self):
        return self.credentials
