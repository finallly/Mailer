import smtplib

fromemail = 'testmailforspamm@mail.ru'
password = 'faksjflkj2348726234SDF'
smtpserver = 'smtp.mail.ru:587'
toemail = 'testmailforspamm@mail.ru'
message = 'testMessage'
amount = 10

server = smtplib.SMTP(smtpserver)
server.starttls()
server.login(fromemail, password)
server.sendmail(fromemail, toemail, message)

for i in range(amount):
    server.sendmail(fromemail, toemail, message)
server.quit()
