#!/usr/bin/env python

import subprocess
import threading
import time
import Queue

'''
    multiple thread-pools with multiple Queues
    we use one thread-pool with qp to get the responding IPs as qa's input,then use
    another thread-pool with qa to get the corrsponding MAC
'''

ping_threads=3
arp_threads=3
IP_LIST=['172.16.24.12','172.16.24.4','172.16.24.8']

def pinger(i,qp,qa):

    while True:
        ip=qp.get()
        print "Thread #%d is pinging %s" % (i,ip)
        cmd="ping -c 1 %s" % ip
        ret=subprocess.call(cmd,shell=True,stdout=open('/dev/null','w'),\
                            stderr=subprocess.STDOUT)
        if ret==0:
            qa.put(ip)
            print "[+] %s is up" % ip
        else:
            print "[-] %s is not respond" % ip

        qp.task_done()

def arper(qa):

    while True:
        try:
            ip=qa.get()
            print "%s is being arped" % (ip)
            cmd="arp %s | tail -n 1| awk '{print $3}' " % ip
            out=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,\
                             stderr=subprocess.PIPE)
            mac=out.stdout.read()
            print "IP Address: %s | Mac Address: [ %s ]" % (ip,mac)
        except:
            print "error occured"
        finally:
            qa.task_done()

def main():
    qp=Queue.Queue()
    qa=Queue.Queue()
    
    for i in range(ping_threads):
        worker=threading.Thread(target=pinger,args=(i,qp,qa))
        worker.setDaemon(True)#stop main thread from infinite waiting
        worker.start()

    for i in range(len(IP_LIST)):
        qp.put(IP_LIST[i])

    for i in range(arp_threads):
        worker=threading.Thread(target=arper,args=(qa,))
        worker.setDaemon(True)
        worker.start()

    print "Main Thread starting"
    qp.join()#block the main thread until all of the element runs q.task_done() on time
    qa.join()
    print 'done'

if __name__=="__main__":
    main()
