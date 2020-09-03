from smtplib import SMTPConnectError, SMTPAuthenticationError, SMTPDataError, SMTPServerDisconnected, SMTPSenderRefused


class errorHandler(object):

    def __init__(self, error):
        print(error)
        print(type(error))