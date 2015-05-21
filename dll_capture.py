#!/usr/bin/env python

import os
import socket
import sys

'''
    Ehternet layer capture
'''

def show_details(msg):
    '''show the details in hexdecimal type of one packet'''
    
    msg_len=len(msg[0])
    print "msg length is %d, and details are:" % msg_len
    lines=msg_len//8+1
    for i in range(lines):
        for j in range(8):
            index=i*8+j
            if index>=msg_len:
                break;
            char=ord(msg[0][index])
            if char&0xf0==0:
                hex_str="0%0x\t" % char
            else:
                hex_str="%0x\t" % char
            print hex_str,
        print ''


def main():
    if len(sys.argv)!=3:
        print "Usage:./dll_capture Host [IP|ARP]"
        sys.exit(1)

    host=sys.argv[1]
    protocol=sys.argv[2]

    if protocol=="IP":
        socket_protocol=0x0800
        print "Caputre IP packets"
    elif protocol=="ARP":
        socket_protocol=0x0806
        print "Capture ARP packets"

    sock=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(socket_protocol))
    msg=sock.recvfrom(128)
    if msg!=None:
        show_details(msg)

if __name__=="__main__":
    main()

