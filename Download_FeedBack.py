#!/usr/bin/env python
# coding: utf-8


import imaplib, email, json
import pandas as pd


def Authenticate(login, password, verbose=True):
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        rslt, _ = M.login(login, password)
        if rslt=='OK' and verbose:
            print("\r     [+]  Login Successful ", end='')
    except:
        if verbose:
            print("\r     [!]  Login Failed  ", end='')
        return False
    else:
        return M

def extractData(M, e_id):
    rslt, data = M.uid('fetch', e_id, '(RFC822)')
    email_msg = email.message_from_bytes(data[0][1])
    for part in email_msg.walk():
        data = part.get_payload()

        Cname, Cemail, Cfb = tuple(data.split("<<::>>"))

        return formatName(Cname, rep="Name:"), formatName(Cemail, rep="Email_Address:"), formatName(Cfb, rep="Comment:")

        
def formatName(name, rep):
    return name.replace(rep, "").replace("_", " ").strip()

usrname = 'rebellocleophas731@gmail.com'
passwd = "gcniboutzdkzfyyg"

M = Authenticate(usrname, passwd)
M.select('inbox')

sub = "Customer FeedBack"
rslt, data = M.uid('search', None, f'SUBJECT "{sub}"')

id_lists = data[0].split()

data = []
for idx, e_id in enumerate(id_lists):
    print(f"\r *Fetching emails  {idx+1}/{len(id_lists)}", end="")
    data.append(extractData(M, e_id))

df = pd.DataFrame(data, columns=["Name", "Email", "Feedback"])
df.to_json("UserFeedBack.json")
