#!/usr/bin/env python
'''
    tcp conncect scan with python
    violent_python@2014-09-01
'''

import optparse
import socket
import threading

screenLock=threading.Semaphore(1)

def connScan(tgtHost,tgtPort):
    try:
        connSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connSock.connect((tgtHost,tgtPort))
        connSock.send("Violent Python\n")
        results=connSock.recv(100)
        screenLock.acquire()
        print "[+] %d/tcp open" % tgtPort
    except:
        screenLock.acquire()
        print "[-] %d/tcp closed" % tgtPort
    finally:
        screenLock.release()
        connSock.close()

def portScan(tgtHost,tgtPorts):
    try:
        tgtIP=socket.gethostbyname(tgtHost)
    except:
        print "can't resolve the %s ,unknown host" % tgtHost
        return

    print "[+] Scan Results for: %s" % tgtIP
    tgtPorts=tgtPorts.split(',')
    for tgtPort in tgtPorts:
        t=threading.Thread(target=connScan,args=(tgtIP,int(tgtPort)))
        t.start()

def main():
    parser=optparse.OptionParser('usage <-H Host> <-P ports> sepearted with comms')
    parser.add_option('-H',dest='tgtHost',type='string')
    parser.add_option('-P',dest='tgtPorts',type='string')
    (options,args)=parser.parse_args()
    tgtHost=options.tgtHost
    tgtPorts=options.tgtPorts
    if(tgtHost == None) or (tgtPorts == None):
        print parser.usage
        exit(0)
    portScan(tgtHost,tgtPorts)

if __name__=="__main__":
    main()
        
