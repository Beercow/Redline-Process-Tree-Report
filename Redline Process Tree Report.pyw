#Textentrybox1.py 
from Tkinter import *
import tkFileDialog 
import csv
import re
import graphviz as gv
import functools
import os

csv.field_size_limit(sys.maxsize)

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

    with open(val1, 'rb') as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if row['Field'] == 'ProcessAgentEvent/Start/Generated']

    for row in rows:
        test = str(row['Summary'])
        keys = re.split('(parent [a-z0-9]+: |[a-z0-9]+: )(?i)',test)
        pair = zip(*[iter(keys[1:])]*2)
        pp = str(pair[8][1]).split('\\')[-1]
        p = str(pair[0][1]).split(' ')[0]
        g1.edge(('{0}\\n{1}'.format(pp , pair[7][1] )),('{0}\\n{1}'.format(p , pair[2][1] )))
    g1.node_attr={'shape': 'box'}
    g1.render(temp, view=True, cleanup=True)

def main():   
    root = Tk()  # Create the root (base) window where all widgets go 
    root.title('Redline Process Tree Viewer')
#    root.iconbitmap(default=sys._MEIPASS +'/icon.ico')
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
