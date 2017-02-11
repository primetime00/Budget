from Bank import Bank

class Citi(Bank):
    def __init__(self, credentials):
        Bank.__init__(self, credentials, '2017/02/01')
        self.accountName = "Citi Double Cash Card"
        self.bank = 'citi'
        (self.login, self.password) = self.getLoginInfo()



