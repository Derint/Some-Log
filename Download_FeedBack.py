#!/usr/bin/env python
# coding: utf-8


import imaplib
import email
import bs4
import sys
import os
import re

n = re.compile(r'(?<=Name:).*?(?=\s)')
em = re.compile(r'(?<=Email Address:).*?(?=\s)')
c = re.compile(r'(?<=Comment:).*?(?=\s)')


user = ''
password = ''
m = imaplib.IMAP4_SSL("imap.gmail.com", 993)
m.login(user, password)
m.select('"inbox"')

# search all email and return uids
result, data = m.uid('search', None, f'SUBJECT "Customer FeedBack"')
x = len(data[0].split())
print(f'Found {x} email.')
count = 1

if x > 0:
    with open('Customer Feedback.txt', 'w') as f:
        if result == 'OK':
            for num in data[0].split():
                print(f'\nEmail no: {count}')
                result, data = m.uid('fetch', num, '(RFC822)')

                if result == 'OK':
                    try:
                        email_message = email.message_from_bytes(data[0][1])

                        for part in email_message.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True)
                                bSoup = bs4.BeautifulSoup(
                                    body, features='html.parser')
                                ct = 0
                                for i in bSoup.text.split('<::>'):
                                    i = i.replace('\r', '').replace(
                                        '\n', '').replace('_', ' ')

                                    if n.search(i) != None:
                                        r = n.search(i)

                                    elif em.search(i) != None:
                                        r = em.search(i)

                                    elif c.search(i) != None:
                                        r = c.search(i)

                                    temp = i[r.span()[0]+1:-1]
                                    print(temp)
                                    f.write(temp)

                                    if ct != 2:
                                        f.write('\t')
                                    ct += 1

                                f.write('\n')
                            count += 1

                        print('---------------------' * 5)

                    except Exception as e:
                        print(e)
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(
                            exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
