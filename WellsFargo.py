from Bank import Bank

class WellsFargo(Bank):
    def __init__(self, credentials):
        Bank.__init__(self, credentials, '2017/02/01')
        self.accountName = "EVERYDAY CHECKING"
        self.bank = 'wells'
        (self.login, self.password) = self.getLoginInfo()


