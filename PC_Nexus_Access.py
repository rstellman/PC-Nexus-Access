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
Date:  28 Nov 2012  -- R. Stellman [ Cleaned up menu ]
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Menu
from Tkinter import *
import Tkinter
from Tkconstants import *
import ScrolledText

from Nexus_Object import *
import socket
import os
from datetime import datetime
import time
import shutil
from shutil import *


root= Tk()
root.iconbitmap(default='/root/scripts/py.ico')            # Comment this line out for default icon
fname="/root/scripts/mrun.txt"
text=''
HOSTS= ("172.25.187.155","172.25.187.50","172.25.187.156")
HOST = '172.25.187.155'  
host = HOST
PORT = 50007                       

Nexus1 = Nexus_switch(HOST,PORT)

class Beta(Frame):
   
    
    def __init__(self, parent=None, text='', file=None):

        self.host = HOST
        Frame.__init__(self, parent)           
        self.parent = parent
        self.pack(expand=YES, fill=BOTH)                    
        self.makewidgets()
        self.settext("HOST="+HOST+'\n')
        self.initUI()    

    def callback(self):
        return()
        
    def show(self, fname='/root/scripts/mscript.txt'):
        self.settext(file=fname)
        return(fname)
 
    def initUI(self):

        self.parent.title("PC Nexus Access 1.1a")
        menubar = Menu(self.parent)
        fname='/root/scripts/script.txt'
        self.parent.config(menu=menubar)
        #   st=ScrolledText(root)

        # multimenu and items

        multimenu = Menu(menubar, fg='Blue', tearoff=0)
        multimenu.add_command (label="script",  underline = 0, command=self.display_script)
        multimenu.add_command (label="run",     underline = 1, command=self.display_runlog )      
        multimenu.add_separator()
        multimenu.add_command (label="mscript", underline = 1, command=self.display_mscript)
        multimenu.add_command (label="mrun",    underline = 1, command=self.display_mrunlog)
        multimenu.add_separator()
        multimenu.add_command (label="close",   underline = 0, command=self.close)

        menubar.add_cascade   (label="File",    underline = 1, menu=multimenu  )                              

        #   File menu and menu items
        
        fileMenu = Menu(menubar, fg='Yellow', bg='Blue',tearoff=0)
        fileMenu.add_command (label="Multi",   underline = 0, command=self.run_multiscript)   
        fileMenu.add_command (label='Host0',   underline = 0, command=self.run_host0)           
        fileMenu.add_command (label='Host1',   underline = 0, command=self.run_host1)
        fileMenu.add_command (label='Host2',   underline = 0, command=self.run_host2)
        menubar.add_cascade  (label="Script",  underline = 1, menu=fileMenu   )

        # fileMenu.add_separator()

        menubar.add_command (label="Queues",   underline = 1, command = self.get_queue )                  

        interfacemenu = Menu(menubar,tearoff=0)
        interfacemenu.add_command (label="All  ", underline = 1, command=self.get_interface)                     
        interfacemenu.add_command (label="up   ", underline = 1, command=self.get_interface_up)                     
        interfacemenu.add_command (label="down ", underline = 1, command=self.get_interface_down)
        interfacemenu.add_command (label="vlan ", underline = 1, command=self.get_interface_vlan)
       
        menubar.add_cascade (label="Interface", underline = 1, menu=interfacemenu)                     

        menubar.add_command (label="Buffers",   underline = 1, command=self.get_BMdata)                        
        menubar.add_command (label="Routing",   underline = 1, command=self.get_routing)
        menubar.add_command (label="TCP Sockets",underline = 1, command=self.get_tcp_sockets)     
        menubar.add_command (label="About",     underline = 1, command=self.nexus_about) 
        
    # *******************************************************
    # *               Log Multi-Menu

    def close(self):
        root.destroy()

    def nexus_about (self):
        text = open('/root/scripts/NexusAbout.txt', 'r').read()
        self.settext(text)
    
    def display_script(self):
        text = open('/root/scripts/script.txt', 'r').read()
        self.settext(text)

    def display_mscript(self):
        text = open('/root/scripts/mscript.txt', 'r').read()
        self.settext(text)       

    def display_runlog(self):
        text = open('/root/scripts/run.txt', 'r').read()                
        self.settext(text)

    def display_mrunlog(self):
        text = open('/root/scripts/mrun.txt', 'r').read()                
        self.settext(text)

    # *******************************************************
    def makewidgets(self):
        
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)              # xlink sbar and text
        text.config(yscrollcommand=sbar.set)         # move one moves other
        sbar.pack(side=RIGHT, fill=Y)                # pack first=clip last
        text.pack(side=LEFT, expand=YES, fill=BOTH)  # text clipped first
        self.text = text

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

    def settext(self, text=''):
        
        self.text.delete('1.0', END)                 # delete current text
        self.text.insert('1.0', text)                # add at line 1, col 0
        self.text.mark_set(INSERT, '1.0')            # set insert cursor
        self.text.focus()                            # save user a click
        return(file)
    
    def gettext(self):                               # returns a string
        return self.text.get('1.0', END+'-1c')       # first through last            
     
    def onExit(self):    
        self.quit()
 
    # ---- Nexus CLI ------
    def get_script(self,nexusLogFile = "/bootflash/logs/buffer-nexus.logx"):
        """ Runs the script file on the Nexus Chassis \n"""
      
        bufferText="show host"
      
        try:  buffer1 = open(nexusLogFile,'r')
        except:  return("")
      
        bufferText=buffer1.read()
        buffer1.close()
        return(bufferText)

    def stringNexusCLI (self, sbuffer='',host1=HOSTS[1]):
 
        try:     buffer = repr(Nexus1.s_socket(sbuffer,host1,PORT))
        except:  buffer = "Socket off-line\n  ....\n"         

        return(buffer)
      
    def get_cli_data(self, cli_string="", host1 =HOSTS[1], skip=0):
 
        data = ""
        data = self.stringNexusCLI(cli_string,host1)
        data = 'IP='+host1+'\n\n'+data
        data = Nexus1.stringNexusFormat(data,skip)      
        self.settext(data)
       
        return(data)
         
    def  get_mcli_data(self,  cli_string="", host = HOSTS[1]):       
 
         data = ""
         data = self.stringNexusCLI(cli_string,host)
         data = self.stringNexusFormat(data,0)
         data = data.replace  ('"','\n')
         data = data.replace  ("\n   ","")
         self.settext(data)
         return(data)

    def  get_queue (self):
         host=HOSTS[1]
         buffer = self.get_cli_data ('show platform software qd info global\n', self.host)
         self.settext(buffer)
    #    -----------------------------------------------------------------------------
    def  get_interface (self):
         text = self.get_cli_data ('show int brief\n',self.host)
         self.settext(text)

    def  get_interface_up (self):
         text = self.get_cli_data ('show int status up \n',self.host)
         self.settext(text)

    def  get_interface_down (self):
         text = self.get_cli_data ('show int status down \n',self.host)
         self.settext(text)

    def  get_interface_vlan (self):
         text = self.get_cli_data ('show vlan \n',self.host)
         self.settext(text)
   
    #    -----------------------------------------------------------------------------
    def  get_BMdata (self):
         text = self.get_cli_data ('BMdata',self.host,1)
         self.settext(text)
        
    def  run_script (self, host):
         # Runs current Host script
         bufferText = self.get_script('/root/scripts/script.txt')                             
         text = self.get_cli_data (bufferText,self.host,0)
         self.settext(text)
         Nexus1.s_write ("/root/scripts/run.txt", text)
         return(host)
   
    def  run_multiscript (self):
   
         bufferText = self.get_script('/root/scripts/mscript.txt')  
         #HOSTS=("172.25.187.155","172.25.187.50","172.25.187.155")                            
         bufferm = "Multi Script \n"
         bufferm = bufferm + '\n'+HOSTS[0] + '\n '+ self.get_mcli_data (bufferText,HOSTS[0]) 
         bufferm = bufferm + '\n'+HOSTS[1] + '\n '+ self.get_mcli_data (bufferText,HOSTS[1]) 
         bufferm = bufferm + '\n'+HOSTS[2] + '\n '+ self.get_mcli_data (bufferText,HOSTS[2])                                   
         Nexus1.s_write ("/root/scripts/mrun.txt", bufferm)
         self.settext(bufferm)
   
    def  get_routing (self):
         text = self.get_cli_data ('sh ip route vrf management\n',self.host,0)
         self.settext(text)

    def  run_host0 (self):
         self.host = HOSTS[0]
         self.host = self.run_script(self.host)
   
    def  run_host1 (self):
         self.host = HOSTS[1]
         self.host = self.run_script(self.host)
             
    def  run_host2 (self):
         self.host = HOSTS[2]
         self.host = self.run_script(self.host)
        
    def  get_tcp_sockets(self):
         text = self.get_cli_data ('show sockets connection tcp\n',self.host,0)
         self.settext(text)
          
# ----------------------------------------------------------------------------------
#       Main -----------

def main():
 
    root.geometry("800x550+300+300")
    app = Beta(root)
    
    #fname= app.settext()
    #text = open(fname, 'r').read()                   

    root.mainloop()  


if __name__ == '__main__':
    main()  
