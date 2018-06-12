'''
The facade pattern is used to provide a simple interface to a complex system
of components. There often are 'typical' usages of complex systems - the facade
allows us to define a new object that encapsulates this typial usage of a system.
'''
import smtplib
import imaplib

'''
smtplib and imaplib normally provide only a thin layer of abstraction for those
protocols. We can use a facade pattern to make sending and receiving emails
easier.
'''


class EmailFacade:

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, message):
        if not '@' in self.username:
            from_email = "{0}@{1}".format(self.username, self.host)
        else:
            from_email = self.username
        message = ("From: {0}\r\n"
                "To: {1}\r\n"
                "Subject: {2}\r\n\r\n{3}").format(
                from_email,
                to_email,
                subject,
                message)

        smtp = smtplib.SMTP(self.host)
        smtp.login(self.username, self.password)
        smtp.sendemail(from_email, (to_email,), message)

    def get_inbox(self):
        mailbox = imaplib.IMAP4(self.host)
        mailbox.login(bytes(self.username, 'utf8'),
            bytes(self.password, 'utf8'))
        mailbox.select()
        x, data = mailbox.search(None, 'ALL')
        messages = []
        for num in data[0].split():
            x, message = mailbox.fetch(num, '(RFC822)')
            message.append(message[0][1])
        return messages
