#!/usr/bin/env python
#
#  SocketServerx .py,pyc
#  Author:  Robert Stellman (rostellm)
#  Date  :  27 Sep 2012 -  New file from NexusAccess.py
#
#  Date  :  01 Oct 2012 -  Added Try for the connection send 
#

from cisco import *
from datetime import datetime
import time
from socket import *            # get socket constructor and constants
from sys import *
from string import join

myHost = '172.25.187.155'       # '' = all available interfaces on host
myPort = 50007                  # listen on a non-reserved port number

# get ouput of CLI command
oCli = CLI("show int mgmt0 brief | grep mgmt0", False)       
              
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

# make a TCP socket object   
# bind it to server port number	
# listen, allow 5 pending connects

sockobj = socket(AF_INET, SOCK_STREAM)          
sockobj.bind((myHost, myPort))                  
sockobj.listen(5)                               

def get_buffer_monitor_output(BMcli, bufferValues):
    curDate=datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
    BMcli.rerun()
    f, m, bUsage = BMcli.get_raw_output().split("\n")[4].rpartition(' ')
    bufferValues.append(curDate + "," + bUsage)
    time.sleep(1)
    return(bufferValues)

bufferValues = []



BMcli = CLI('show hardware internal buffer info pkt-stats brief', False)
counter = 0

while True:  # listen until process killed

      #  collect buffer monitor data
      #  bufferValues = get_buffer_monitor_output(BMcli, bufferValues)
      
      curDate=datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
      BMcli.rerun()
      f, m, bUsage = BMcli.get_raw_output().split("\n")[4].rpartition(' ')
      bufferValues.append(curDate + ": " + bUsage+"\n")
      time.sleep(1)
      
      bvCount=len(bufferValues)

      connectionFailed = False
      curDate=datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
     
      # In case of no connection requests -
      try:
           connection, address = sockobj.accept() 
      except timeout, msg:
           connectionFailed = True                        
           pass
              
      if ( connectionFailed != True ):
      
	 # read next line on client socket
         data = connection.recv(1024)            
  
         if (data == "BMdata"):
             
            BMdata = 20
            bvCount=len(bufferValues)
            if (bvCount < BMdata): BMdata = bvCount
            if (bvCount > 20): BMdata=20
            
            # Send out the values
             
            if ( BMdata > bvCount ): 
                 cerror =  "  Invalid index"
                 connection.send("bvCount="+repr(bvCount)+cerror)    
            else:
                 n = bvCount-BMdata
                 connection.send(join(bufferValues[n:bvCount]))
		   
         # get ouput of CLI command 
         
         if (data != "BMdata"):             
            oCli = CLI(data, False)                 
            
            buffer=repr(oCli.get_output())
            
            # until eof or  socket closed
            
            try:     connection.send(buffer)                 
            except:  connection.close()
             
         connection.close()

