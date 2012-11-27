#!/usr/bin/env python
#
#  SocketServer_N5K.py,pyc
#  Author:  Robert Stellman (rostellm)
#  Date  :  27 Sep 2012 -  New file from NexusAccess.py
#           16 Nov 2012 -  N5K version (buffer monitor removed, commands not applicable on N5K)
#  Date  :  01 Oct 2012 -  Added Try for the connection send 
#

"""
***************************************************************************************************
The script examples provided by Cisco for your use are provided for
reference only as a customer courtesay.

They are intended to facilitate development of your own scripts and software
that interoperate with Cisco switches and software.

Although Cisco has made efforts to create script examples that will be effective
as aids to script or software development,

Cisco assumes no liability for or support obligations related to the use of the script examples or
any results obtained using or referring to the script examples.

***************************************************************************************************

"""



from cisco import *
from datetime import datetime
import time
from socket import *            # get socket constructor and constants
from sys import *
from string import join

myHost = '172.25.187.155'       # '' = all available interfaces on host
myPort = 50007                  # listen on a non-reserved port number


oCli = CLI("show int mgmt0 brief | grep mgmt0", False)       # get ouput of CLI command
              
buffer = repr(oCli.get_output()) 

buffer = buffer.replace  ('[','')            
buffer = buffer.replace  ("']",'')
buffer = buffer.replace  ("'"," ")
buffer = buffer.replace  ('\\',' ')
buffer = buffer.replace  (' ,','\n')


buffer = buffer.replace ("mgmt0","")
buffer = buffer.replace ("--","")
buffer = buffer.replace ("up","")
buffer = buffer.lstrip()
buffer = buffer.split(" ")[0]     

myHost = buffer

sockobj = socket(AF_INET, SOCK_STREAM)          # make a TCP socket object
sockobj.bind((myHost, myPort))                  # bind it to server port number
sockobj.listen(5)                               # listen, allow 5 pending connects


while True:                                             # listen until process killed


        connectionFailed = False
        curDate=datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

        try:
                connection, address = sockobj.accept() 
        except timeout, msg:
                connectionFailed = True                         # In case of no connection requests -
                pass
                
        if ( connectionFailed != True ):
        
        
               data = connection.recv(1024)                    # read next line on client socket
  
               if (data == "BMdata"):
                   connection.send("Not Available: N5K")     # Send out the values
		   
                          
               if (data != "BMdata"):             
                   oCli = CLI(data, False)                     # get ouput of CLI command
               
                   buffer=repr(oCli.get_output())
               
                   try:  connection.send(buffer)               # until eof when socket closed
                   except:  connection.close()
               
               connection.close()

