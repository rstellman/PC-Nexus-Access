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
Menu - Beta Script - Test Prototype
*** Combine Scrolled Text with Example Frame as Main Frame
Date:  26 Nov 2012  -- R. Stellman
"""

# Nexus_Object.py program

import socket

import os
from datetime import datetime
import time
import shutil
from shutil import *


class Nexus_switch:

      def __init__(self, host, port):
          HOST = host              # The remote host
          PORT = port              # The same port as used by the server


      def s_socket(self,sbuffer,HOST,PORT):
          # Sends the buffer to the server
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.connect((HOST, PORT))
          s.sendall(sbuffer)
          data = s.recv(6500)
          s.close()

          return(data)

      def s_read (self,fname = "a.tmp"):
          # Loads a file into the buffer string
          #
          nexusLogFile = fname
          bufferText=" ... "
          buffer1 = open(nexusLogFile,'r')
          bufferText = buffer1.read()
          buffer1.close()

          return(bufferText)

      def s_write (self,fname= "/bootflash/a.tmp", bufferText=""):
          # ... Write to a file
          #
          bufferFile = open(fname, 'w')
          bufferFile.write(bufferText)
          bufferFile.close()
          
          return()

      def stringNexusFormat (self, bufferText, skip=0):
          """\n  Format file data for Humans     """
          bufferText = bufferText.replace  ('"[','')            
          bufferText = bufferText.replace  (']','')
          bufferText = bufferText.replace  ("'"," ")
          bufferText = bufferText.replace  ('\\',' ')
          bufferText = bufferText.replace  ('",','"\n')         # Needed for 'show routes'
          bufferText = bufferText.replace  (' ,','\n')
        
          if (skip == 1):  # Buffer Monitor; csv data
                         bufferText = bufferText.replace  (' n','\n')
                         
          return (bufferText)
          