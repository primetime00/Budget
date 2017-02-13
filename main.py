from WellsFargo import WellsFargo
from Citi import Citi
from Budget import Budget
from Email import Email

budget = Budget()
email = Email(budget.getEmail())

wf = WellsFargo(budget.getCredentials())
citi = Citi(budget.getCredentials())


citi.requestTransactions()
budget.updateCredentials(citi.getCredentials())
citi.processTransactions()
citi.setExpenses(budget.getExpenses())
citi.setExclusions(budget.getExclusions())


wf.requestTransactions()
wf.processTransactions()
wf.setExpenses(budget.getExpenses())
wf.setExclusions(budget.getExclusions())

spending = citi.getSpending() + wf.getSpending()

balance = budget.getCalculatedTotal() - spending
email.sendReport(balance)

print("You Remaining: {}".format(budget.getCalculatedTotal() - spending))




