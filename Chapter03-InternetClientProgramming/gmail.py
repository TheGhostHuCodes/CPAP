#!/usr/bin/env python3

import getpass
from smtplib import SMTP

who = input("email-address: ")
# If using 2FA you may need an application password.
password = getpass.getpass()
from_ = who
to = [who]

headers = ['From: {}'.format(from_),
           'To: {}'.format(','.join(to)),
           'Subject: test SMTP send via 587/TLS', ]
body = ['Hello',
        'World!', ]
msg = '\r\n\r\n'.join(('\r\n'.join(headers), '\r\n'.join(body)))


def get_subject(msg, default='(no subject line)'):
    for line in msg:
        if line.startswith('Subject:'):
            return line.rstrip()
        if not line:
            return default


print("*** Doing SMTP send via TLS...")
s = SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(who, password)
s.sendmail(from_, to, msg)
s.quit()
print("*** TLS mail sent!")
