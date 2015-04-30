#!/usr/bin/env python

from synscan_with_rawsocket import *
import threading
import Queue


def scan(srcip,dstip,q):
    while True:
        port=q.get()
        print "processing port %d" % port
        scanner(srcip,dstip,port)
        q.task_done()


def main():

    p=optparse.OptionParser(description='use syn packet to scan selected ports',\
                            usage='''./syncan_with_rawsocket.py -s srcip -d
                            dstip -sp startport -ep end_port -t thread_number''',\
                            version='1.0.1')
    p.add_option('--source_ip','-s',dest='source_ip',type='string',\
                 action='store',help='set the source ip')
    p.add_option('--destination_ip','-d',dest='destination_ip',type='string',\
                 action='store',help='set the destination ip')
    p.add_option('--start_port','-f',dest='startport',type='int',\
                 default=0,action='store',help='set the fisr\start port')
    p.add_option('--end_port','-e',dest='endport',type='int',\
                 default=65535,action='store',help='set the end port')
    p.add_option('--thread_number','-t',dest='thread_number',type='int',\
                  default=1,action='store',help='set the thread number')

    opts,args=p.parse_args()
    source_ip=opts.source_ip
    destination_ip=opts.destination_ip
    start_port=opts.startport
    end_port=opts.endport
    thread_number=opts.thread_number

    if source_ip==None or destination_ip==None:
        p.print_help()
        exit(1)

    q=Queue.Queue()
    if thread_number>1:
        for i in range(thread_number):
            worker=threading.Thread(target=scan,args=(source_ip,destination_ip,\
                                                      q))
            worker.setDaemon(True)
            worker.start()

        for port in range(start_port,end_port):
            q.put(port)

        q.join()
        print 'all queues has been done'
    else:
        for port in range(start_port,end_port):
            scanner(source_ip,destination_ip,port)
        
if __name__=="__main__":
    main()
