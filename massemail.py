#!/usr/bin/env python

import email
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import encoders
import smtplib
import mimetypes
import base64
import threading
import optparse
import time


email_count=1

def send_email():
    global email_count
    to_addr="956478752@qq.com"
    from_addr="15165268607@163.com"
    subject_header="Subject: Sending PDF Attachment"
    attachment='/home/wolf/python_books/cdn_list.pdf'
    body='This message sends a PDF attachment'

    #MIMEMultipart can consist of different types of message
    #multipart/* type
    m=MIMEMultipart()
    m['To']=to_addr
    m['From']=from_addr
    m['Subject']=subject_header

    #get the attachment's maintype and subtype
    ctype,encoding=mimetypes.guess_type(attachment)
    print ctype,encoding
    maintype,subtype=ctype.split('/',1)
    print maintype,subtype

    #add the payload to the current payload
    #MIMEText Text/* type
    m.attach(MIMEText(body))
    fp=open(attachment,'rb')
    #Base class for MIME specialization,set the content-type
    msg=MIMEBase(maintype,subtype)
    msg.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(msg)
    msg.add_header('Content-Disposition','attachment',filename=attachment)
    m.attach(msg)

    user="15165268607@163.com"
    passwd="!junshuai1"
    s=smtplib.SMTP('smtp.163.com')
    print 'successfully connect to 163 smtp mail server'
    #s.set_debuglevel(1)
    s.docmd('EHLO server')
    #adapt SSL
    s.starttls()
    s.docmd('AUTH LOGIN')
    s.send(base64.encodestring(user))
    s.getreply()
    s.send(base64.encodestring(passwd))
    s.getreply()
    print 'login successuful'
    s.sendmail(from_addr,to_addr,m.as_string())
    print 'send successful'
    email_count+=1
    s.quit()

def send_cycle(thread_num):
    while True:
        send_email()

def send_threads(thread_num):
    start=time.time()
    thread_list=[]
    for i in range(thread_num):
        t=threading.Thread(target=send_cycle,args=(i,))
        thread_list.append(t)

    for i in range(thread_num):
        thread_list[i].start()

    for i in range(thread_num):
        thread_list[i].join()
    end=time.time()
    period='%.2f' % (end-start)
    print 'Send %d emails totally in %.2f' % (email_count,period)

def main():
    p=optparse.OptionParser(description='send mass emails to one user',\
                            version='1.0',prog='massemail',\
                            usage='python massemail.py -n thread_number')
    p.add_option('--thread_number','-n',dest='thread_number',\
                 type='int',action='store',\
                 help="set the number of threads")
    opts,args=p.parse_args()
    thread_number=opts.thread_number
    if thread_number==None:
        p.print_help()
    else:
        send_threads(thread_number)
        
if __name__=="__main__":
    main()













