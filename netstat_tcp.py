#!/usr/bin/env python

import re
import string
import time
import sys

STATE={
	'01':'ESTABLISHED',
	'02':'SYN_SENT',
	'03':'SYN_RECV',
	'04':'FIN_WAIT1',
	'05':'FIN_WAIT2',
	'06':'TIME_WAIT',
	'07':'CLOSED',
	'08':'CLOSE_WAIT',
	'09':'LAST_ACK',
	'0A':'LISTEN',
	'0B':'CLOSING'
	}

def get_port(port):
	return str(string.atoi(port,base=16))

def get_ip(ip):
	dot_list=[ip[i*2 : (i+1)*2] for i in range(0,len(ip)/2)]
	decimals=[string.atoi(dot_list[i],base=16) for i in range(0,len(dot_list))]
	decimals=[str(item) for item in decimals]
	ip_str='.'.join(decimals)
	return ip_str

def get_queue(queue):
	return str(string.atoi(queue,base=16))

def get_out_put(line):
	line=line.strip()
	info_list=re.split('\s+',line)
	src_ip_port=(info_list[1]).split(':')
	src_ip=get_ip(src_ip_port[0])
	src_port=get_port(src_ip_port[1])
	dst_ip_port=(info_list[2]).split(':')
	dst_ip=get_ip(dst_ip_port[0])
	dst_port=get_port(dst_ip_port[1])
	state=STATE[info_list[3]]
	queues=info_list[4].split(':')
	recvq=get_queue(queues[0])
	sendq=get_queue(queues[1])
	pid=info_list[7]
	#out_str='tcp'+'  '+pid+'  '+recvq+'  '+sendq+'  '+src_ip+':'+src_port+' '*10+dst_ip+':'+dst_port+' '*10+state
	#print out_str
	print "tcp  ",
	print "%-6s%-8s%-8s%-24s%-24s%s" % (pid,recvq,sendq,src_ip+":"+src_port,dst_ip+":"+dst_port,state)

def summarise(continous_flag,interval):
	while 1:
		f=open('/proc/net/tcp')
		f.readline()
		for line in f.readlines():
			get_out_put(line)
		f.close()
		if continous_flag==1:
			time.sleep(interval)
			print ''
		else:
			break

def main():
	continous_flag=0
	interval=0
	if len(sys.argv)==3:
		if sys.argv[1]=="-i":
			continous_flag=1
			interval=string.atoi(sys.argv[2])
		else:
			print "Usage: ./netstat -i interval"
			sys.exit(1)

	print "Active Internet connections (servers and established)"
	print "Proto  PID  Recv-Q  Send-Q  Local Address         Foreign Address          State"
	summarise(continous_flag,interval)
	

if __name__=="__main__":
	main()

