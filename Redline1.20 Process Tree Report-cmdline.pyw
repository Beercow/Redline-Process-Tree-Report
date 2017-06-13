## Redline 1.20 supports process cmdline, and this creates process with cmdline
## Read [Agent Events] - [Process Events]
# -*- coding: utf-8 -*-

#Textentrybox1.py 
from Tkinter import *
import tkFileDialog 
import csv
import re
import graphviz as gv
import functools
import os
import sys

#import pdb; pdb.set_trace()

#csv.field_size_limit(sys.maxsize)
csv.field_size_limit(2147483647) # for 64bit

def buttonPushed(file_name): 
    name = tkFileDialog.askopenfilename(initialdir=(os.getenv('USERPROFILE')+'/Desktop/'), filetypes=(('CSV','*.csv'),('All Files', '*.*')))
    file_name.set(name)
    
def createTextBox(parent,file_name):
    getFile = Entry(parent, width=40, textvariable=file_name) 
    getFile.pack() 

def show_entry_fields(val1):
    print val1
    temp = os.getenv('TMP')+'\\Process Tree'
    digraph = functools.partial(gv.Digraph, format='svg')
    g1 = digraph()

    # Read Process tree CSV files
    with open(val1, 'rb') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row['Action'] == 'start']
        for row in rows:
            cmdline = ''
            ppname = str(row['Parent Name'])
            ppid = str(row['Parent PID'])
            pid = str(row['PID'])
            pname = str(row['Process Name'])
            cmdline = str(row['Command Line'])
            cmdline = cmdline.replace('\\','\\\\')
            
            # remove unnecessary process
            if pname == 'xagt.exe' or ppname == 'xagt.exe':
                continue
            if pname == 'bash.exe' or ppname == 'bash.exe':
                continue
            
            # Make Process Node
            if cmdline != '':
                A = ('{0}\\n{1}'.format(ppid, ppname))
                B = ('{0}\\n{1}'.format(pid, pname))
                g1.node(A, ('{0}\\n{1}\\n{2}'.format(ppid, ppname, cmdline)))
                g1.node(B, ('{0}\\n{1}'.format(pid, pname)))
                g1.edge(A, B)
#                g1.edge('{0}\\n{1}'.format(ppid, ppname),('{0}\\n{1}'.format(pid, pname)),('{0}'.format(cmdline)))
            else:
                g1.edge('{0}\\n{1}'.format(ppid, ppname),('{0}\\n{1}'.format(pid, pname)))
        
    g1.node_attr={'shape': 'box'}
    g1.render(u'temp', view=True, cleanup=True)
      

def main():   
    root = Tk()  # Create the root (base) window where all widgets go 
    root.title('Redline Process Tree Viewer')
    root.resizable(width=FALSE, height=FALSE)
    file_name = StringVar(None)
    b1 = Button(root, text="Select Redline csv:",command=lambda: buttonPushed(file_name)) 
    b1.pack(side=LEFT)
    getFile = Entry(root, width=40, textvariable=file_name) 
    getFile.pack(side=LEFT, fill=Y)
    b2 = Button(root, text='Run', command=lambda: show_entry_fields(getFile.get()))
    b2.pack(side=LEFT)
    root.mainloop() # Start the event loop 

main() 
