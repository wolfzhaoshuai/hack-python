#/usr/bin/env python

import os

print "Monitoring broadcast packets on the network"
#b1='tshark -i eth0 -R"eth.dst==FF:FF:FF:FF:FF:FF" -a duration:90 > output.txt'
#b2='tshark -i eth0 -R"ip.dst==172.16.24.12 && icmp.type==8" -a duration:30>output.txt'
os.popen(b2)
#f=open("output.txt",'r')
print "To view the type of broadcasts open the file output.txt"
