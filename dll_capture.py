#!/usr/bin/env python

import os
import socket
import sys
import string

'''
    Ehternet layer capture
'''

def show_details(msg):
    '''show the details in hexdecimal type of one packet'''
	
	#get pritable chars set
    printable=[]
    for item in string.printable:
	printable.append(ord(item))    

    msg_len=len(msg[0])
    print "msg length is %d, and details are:" % msg_len
    lines=msg_len//8+1
    for i in range(lines):
        str_line=[]
        for j in range(8):
            index=i*8+j
            if index>=msg_len:
                break;
            char=ord(msg[0][index])
            if char in printable:
                str_line.append(char)
            else:
                str_line.append(256)
            if char&0xf0==0:
                hex_str="0%0x " % char
            else:
                hex_str="%0x " % char
            print hex_str,
        for i in xrange(len(str_line)):
            if str_line[i]==256:
                str_line[i]='.'
            else:
                str_line[i]=chr(str_line[i])
        print ' '.join(str_line)


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

