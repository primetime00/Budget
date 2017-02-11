import smtplib

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
            print 'successfully sent the mail'
        except:
            print "failed to send mail"
