#!/usr/bin/env python

import sys
import socket
import getopt
import threading
import subprocess

#define some global variables
listen             = False
command            = False
target             = ""
port               = 0

def usage():
    print "Usage: usage Usage:enter -h or --help to get the usage"
    print "Options:"
    print "-h, --help    show this help message and exit"
    print "-t TGT, --target=TGT    the target host"
    print "-p PORT, --port=PORT    the listen port"
    print "-l LISTEN, --listen=LISTEN    turn on/off listen mode"
    print "-c COMMAND, --command=COMMAND    turn on/off command mode"

def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        print "[+]Connected to %s:%d successfully" % (target,port)

        if len(buffer):
            client.send(buffer)

        while True:
            response=''
            recv_len=1
            while recv_len:
                data=client.recv(4096)
                recv_len=len(data)
                response+=data
                if recv_len<4096:
                    break
            print response

            buffer=raw_input("")
            buffer+="\n"

            client.send(buffer)
    except:
        print "[-] Exception Occured. Exiting"

        #close the connection
        client.close()

def server_loop():
    global target

    if not len(target):
        target="0.0.0.0"

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket,addr=server.accept()
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def run_command(command):
    #trim the newline and space at head and end
    command=command.strip()

    #run the command and receive the output
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="Failed to execute the command: %s.\r\n" % command

    return output

def client_handler(client_socket):

    global command
    
    if command:
        while True:
            client_socket.send("<Your Command> ")
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)

            response=run_command(cmd_buffer)

            client_socket.send(response)


def main():
    global listen
    global command
    global target
    global port

    if not len(sys.argv[1:]):
        usage()

    try:
        opts,args=getopt.getopt(sys.argv[1:],"hlt:p:c",\
                                ["help","listen","target","port","command",])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen=True
        elif o in ("-c","--command"):
            command=True
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            port=int(a)
        else:
            assert False,"Unhandled Option"

    #are we going to listen or just send data from stdin?
    if not listen and len(target) and port>0:
        #read in the buffer from the commandline
        #this will block,please push Ctrl-D
        buffer=sys.stdin.read()
        client_sender(buffer)
    if listen:
        server_loop()

main()
