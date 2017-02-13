import smtplib
from datetime import date

class Email:
    def __init__(self, email):
        self.email = email

    def send(self, recipient, subject, body):

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        gmail_user = self.email["user"]
        gmail_pwd = self.email["pass"]


        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = ", ".join(recipient) if type(recipient) is list else recipient

        html = body

        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(gmail_user, recipient if type(recipient) is list else [recipient], msg.as_string())
            server.close()
            print('successfully sent the mail')
        except:
            print("failed to send mail")

    def sendReport(self, balance):
        bstr = format(balance, '.2f')
        send_to = self.email["subscribers"]
        subject = "${} remaining for the month!".format(bstr)
        body = self.generateBody(balance)
        self.send(send_to, subject, body)

    def generateBody(self, balance):
        bstr = format(balance, '.2f')
        body = '<html><head>{}</head><body>'.format(self.insertStyle())
        body += '<h2>BUDGET REPORT for {}</h2><br>'.format(date.today().strftime("%B"))
        body += 'Our remaining balance for the month is: '
        if balance < 300:
            body += '<div class="cash-bad">${}</div><br>'.format(bstr)
            body += 'At this rate there will be no vacations anytime soon!'
        else:
            body += '<div class="cash">${}</div><br>'.format(bstr)
            body += 'Keep saving and we can go on a vacation!'
        body += "</body></html>"
        return body

    def insertStyle(self):
        s = '<style>'
        s+= '.cash { color: green; display: inline; font-weight: bold;}'
        s += '.cash-bad { color: red; display: inline; font-weight: bold;}'
        s+='</style>'
        return s
