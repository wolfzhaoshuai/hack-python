#!/usr/bin/env python

'''
    Use raw sockets to create tcp/ip packets. The packet=ip packet+tcp packet
    +data
'''

import socket
import struct


def check_sum(msg):
    '''
        function to calculate the check_sum_number
    '''

    s=0
    #when calculate,use 16bits every time
    for i in range(0,len(msg),2):
        w=(ord(msg[i])<<8)+(ord(msg[i+1]))
        s=s+w
        
    s=(s >>16)+(s&0xffff)#?
    s=~s & 0xffff

    return s
    
        
def create_ip_header(source_ip,dest_ip):
    
    #ip header
    ip_version=4
    ip_ihl=5 #the length of ip packet header
    ip_ttl=255
    ip_tos=0
    ip_total_len=40 #tcp_header+ip_header
    ip_id=12345
    ip_flag_fragment_offset=0
    ip_protocol=socket.IPPROTO_TCP
    ip_check=10
    ip_source_addr=socket.inet_aton(source_ip)
    ip_dest_addr=socket.inet_aton(dest_ip)
    #in model struct,the min data-type-length is 8bit
    ip_version_ihl=(ip_version<<4)+ip_ihl
    #construct ip header with the above parts
    #the operator '!' inform big-endian(network byte order)
    ip_header=struct.pack("!BBHHHBBH4s4s",ip_version_ihl,ip_tos,ip_total_len,ip_id,\
                      ip_flag_fragment_offset,ip_ttl,ip_protocol,ip_check,\
                      ip_source_addr,ip_dest_addr)
    return ip_header

def create_tcp_header(source_ip,dest_ip,dst_port):
    #tcp header
    tcp_source_port=34567
    tcp_seq_number=0
    tcp_ack_number=0
    tcp_ihl=5 #the length of tcp packet header
    tcp_urg=0
    tcp_ack=0
    tcp_psh=0
    tcp_rst=0
    tcp_syn=1
    tcp_fin=0
    tcp_window_size=socket.htons(8192) #very important
    tcp_check=0
    tcp_urg_ptr=0
    tcp_ihl_reserved=(tcp_ihl<<4)+0
    tcp_flags=(tcp_urg<<5)+(tcp_ack<<4)+(tcp_psh<<3)+(tcp_rst<<2)+\
               (tcp_syn<<1)+tcp_fin
    #construct tcp header with the above parts
    tcp_header=struct.pack("!HHLLBBHHH",tcp_source_port,dst_port,tcp_seq_number,\
                       tcp_ack_number,tcp_ihl_reserved,tcp_flags,\
                       tcp_window_size,tcp_check,tcp_urg_ptr)


    #pseudo header fields ???
    source_addr=socket.inet_aton(source_ip)
    dest_addr=socket.inet_aton(dest_ip)
    placeholder=0
    protocol=socket.IPPROTO_TCP
    tcp_length=len(tcp_header)
    
    pseudo=struct.pack("!4s4sBBH",source_addr,dest_addr,placeholder,protocol,\
                   tcp_length)
    msg=pseudo+tcp_header
    tcp_check=check_sum(msg)

    #tcp_check=check_sum(tcp_header)
    tcp_header=struct.pack("!HHLLBBHHH",tcp_source_port,dst_port,tcp_seq_number,\
                       tcp_ack_number,tcp_ihl_reserved,tcp_flags,\
                       tcp_window_size,tcp_check,tcp_urg_ptr)
    return tcp_header

def scanner(source_ip,dest_ip,dst_port):
    #construct the raw socket
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_TCP)   
    except:
        print "Could not create thr raw socket"
        exit(1)
    #tell the kernel not to construct IP header,since ourself constructed it
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    ip_header=create_ip_header(source_ip,dest_ip)
    tcp_header=create_tcp_header(source_ip,dest_ip,dst_port)
    packet=ip_header+tcp_header
    s.sendto(packet,(dest_ip,0))
    data=s.recv(1024)

    #transform netdata to hexadecimal format to know it's details
    data_len=len(data)
    print "received %d bytes data" % data_len
    byte_count=data_len/8+1
    for i in xrange(byte_count):
        for j in xrange(8):
            if (i*8+j)==data_len:
                break
            print str(hex(ord(data[i*8+j])))+' '*4,
        print
    print "tcp flag is %d " % ord(data[33])#tcp flag'''
    
    if len(data)==44:
        print "Port %d is open" % dst_port


source_ip="172.16.24.12"
dest_ip="172.16.24.4"
start_port=8007
end_port=8010
for port in range(start_port,end_port):
    scanner(source_ip,dest_ip,port)
    




                       
