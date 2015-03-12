#!/usr/bin/env python

from scapy.all import *
import random
import thread
def worker(source_ip,dest_ip,start_port,end_port):
    print "Running ports %d through %d" %(start_port,end_port)
    for port in xrange(start_port,end_port):
        packet=IP(src=source_ip,dst=dest_ip)/TCP(\
            sport=random.randrange(10000,30000,10),dport=port)
        ans=sr1(packet,verbose=False,timeout=1)
        if ans!=None and ans[TCP].flags==18:
            print "Port: %d is open" % port

source_ip="172.16.24.12"
dest_ip="172.16.24.4"
start_port=8000
end_port=8100
worker(source_ip, dest_ip, start_port, end_port)

 

