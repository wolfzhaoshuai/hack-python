#!/usr/bin/env python

from scapy.all import *
import random
import thread
def worker_syn(source_ip,dest_ip,start_port,end_port):
    print "Running ports %d through %d" %(start_port,end_port)
    for port in xrange(start_port,end_port):
        packet=IP(src=source_ip,dst=dest_ip)/TCP(\
            sport=random.randrange(10000,30000,10),dport=port)
        ans=sr1(packet,verbose=False,timeout=1)
        if ans!=None and ans[TCP].flags==18:
            print "Port: %d is open" % port

def worker_ack(source_ip,dest_ip,start_port,end_port):
    print "Running ports %d through %d" %(start_port,end_port)
    for port in xrange(start_port,end_port):
        packet=IP(src=source_ip,dst=dest_ip)/TCP(dport=port,flags="A")
        ans,unans=sr(packet,verbose=False,timeout=1)
        if ans!=None:
            for s,r in ans:
                print str(s[TCP].dport)+"is unfiltered"
        if unans!=None:
            for s in unans:
                print str(s[TCP].dport)+"is filtered"

def worker_xmas(source_ip,dest_ip,start_port,end_port):
    #xmas scan to find which port is closed
    print "Running ports %d through %d" %(start_port,end_port)
    for port in xrange(start_port,end_port):
        packet=IP(src=source_ip,dst=dest_ip)/TCP(dport=port,flags="FPU")
        ans,unans=sr(packet,verbose=False,timeout=1)
        if ans!=None:
            for s,r in ans:
                print str(s[TCP].dport)+"is closed"

def worker_fin(source_ip,dest_ip,start_port,end_port):
    #xmas scan to find which port is closed
    print "Running ports %d through %d" %(start_port,end_port)
    for port in xrange(start_port,end_port):
        packet=IP(src=source_ip,dst=dest_ip)/TCP(dport=port,flags="f")
        ans,unans=sr(packet,verbose=False,timeout=1)
        if ans!=None:
            for s,r in ans:
                print str(s[TCP].dport)+"is closed"


source_ip="172.16.24.12"
dest_ip="172.16.24.4"
start_port=5000
end_port=8000
worker_xmas(source_ip, dest_ip, start_port, end_port)

 

