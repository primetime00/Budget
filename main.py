from plaid import Client
from plaid import errors as plaid_errors
from pprint import pprint, pformat
from datetime import date
from WellsFargo import WellsFargo
from Citi import Citi
from Budget import Budget

budget = Budget()

wf = WellsFargo(budget.getCredentials())
citi = Citi(budget.getCredentials())


citi.requestTransactions()
citi.processTransactions()
citi.setExpenses(budget.getExpenses())
citi.setExclusions(budget.getExclusions())


wf.requestTransactions()
wf.processTransactions()
wf.setExpenses(budget.getExpenses())
wf.setExclusions(budget.getExclusions())

spending = citi.getSpending()

print("You Remaining: {}".format(budget.getCalculatedTotal() - spending))




