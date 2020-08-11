import smtplib


class smtpConnect(object):

    def __init__(self, server_name, from_mail, password):
        self.server = smtplib.SMTP(server_name)
        self.server.starttls()
        self.server.login(from_mail, password)

    def __enter__(self):
        return self.server

    def __exit__(self, *args):
        self.server.quit()
