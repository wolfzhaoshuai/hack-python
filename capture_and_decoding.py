#!/usr/bin/env python

import socket
import os
import sys
import struct
import string
from ctypes import *

'''
    When the new class have the same methods __new__ and __init__ as metioned in
    the codes,we can use everything whose length is equivalent to the sizeof
    self-defined Ctypes to fill the self-defined structure.Without these two
    methods,you must fill the structure strictly according to the definition
    of every part's type. 
'''


class INADDR(Structure):
    #point out the c_type's bits will help you avoid the error
    #"buffer size too small" in amd64
    _fields_=[
        ("s_addr",c_uint,32)]

class ICMP(Structure):
    _fields_=[
        ("icmp_type",c_ubyte,8),
        ("icmp_code",c_ubyte,8),
        ("icmp_cksum",c_ushort,16)]
    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    def __init__(self,socket_buffer=None):
        pass


class IP(Structure):
    _fields_=[
        ("ip_ihl",c_ubyte,4),
        ("ip_version",c_ubyte,4),
        ("ip_tos",c_ubyte,8),
        ("ip_len",c_ushort,16),
        ("ip_id",c_ushort,16),
        ("ip_off",c_ushort,16),
        ("ip_ttl",c_ubyte,8),
        ("ip_p",c_ubyte,8),
        ("ip_sum",c_ushort,16),
        ("ip_src",c_ulong,32),
        ("ip_dst",c_ulong,32)]

    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self,socket_buffer=None):
        self.protocol_map={1:"ICMP",6:"TCP",7:"UDP"}
        self.src_addr=socket.inet_ntoa(struct.pack("<L",self.ip_src))
        self.dst_addr=socket.inet_ntoa(struct.pack("<L",self.ip_dst))
        try:
            self.protocol=self.protocol_map[self.ip_p]
        except:
            self.protocol=self.ip_p
def main():
    
    if len(sys.argv)!=2:
        print "./capture_and_decoding HostIP"
        sys.exit(1)

    host=sys.argv[1]
    
    #if os type is windows
    if os.name=="nt":
        socket_protocol=socket.IPPROTO_IP
    else:
        socket_protocol=socket.IPPROTO_ICMP
        
    sniffer=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
    #set this option to let packet start from IP_header
    sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
    #sniffer.bind((host,0))
    #if windows,then use ioctl to turn on the NIC in promiscious mode
    if os.name=="nt":
        sniffer.ioctl(socket.SIO_RCVAL,socket.RCVAL_ON)

    try:
        while True:
            packet=sniffer.recvfrom(256)[0]
            #uncomment to know the details in hexadecimal
            '''p_len=len(packet)
            if p_len>30:
                for i in range(25):
                    print "\\x%0x" % ord(packet[i])'''  
            ip_header=IP(packet[0:20])
            offset=(ip_header.ip_ihl)*4

            #another method to know the header length
            #version_and_ihl="%0x" % ord(packet[0])
            #offset=string.atoi(version_and_ihl[1])*4
            
            print "Protocol: %s\t %s ---> %s" % (str(ip_header.protocol),\
                                                 ip_header.src_addr\
                                                 ,ip_header.dst_addr)
            if ip_header.protocol=="ICMP":
                print "IP header's length is %d" % offset
                icmp_header=ICMP(packet[offset:offset+4])
                print "ICMP type is %d, and code is %d" % \
                      (icmp_header.icmp_type,icmp_header.icmp_code)
            print "\n"
    except:
        print sys.exc_info()

        
    if os.name=="nt":
        sniffer.ioctl(socket.SIO_RCVAL,socket.RCVAL_OFF)
        
if __name__=="__main__":
    main()



