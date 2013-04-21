#!/usr/bin/env python
import matplotlib
from random import *
from Tkinter import *
from Referee import *
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure



import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def destroy(e): sys.exit()

class Indicator:
    def __init__(self, master=None, label='', value=0.0, f = 0, t = 100):
        self.var = DoubleVar()
        self.s = Scale(master, 
                 label=label, 
                 variable=self.var,
               from_=f, 
               to=t, 
               orient=HORIZONTAL,
               length=300)
        self.var.set(value)
        self.s.pack()
  
def setTemp():
    slider = choice(range(10))
    value  = choice(range(0, 10))
    slist[slider].var.set(value)
    root.after(5, setTemp)
        
        
root = Tk.Tk()
root.wm_title("Emergence of Money")
 
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0,3.0,0.01)
s = sin(2*pi*t)

a.plot(t,s)
a.set_title('Emergence of Money')
a.set_xlabel('X axis label')
a.set_ylabel('Y label')


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

#toolbar = NavigationToolbar2TkAgg( canvas, root )
#toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
 
slist = []
slist.append(Indicator(master=root, label='Goods')) 


def setCallback():
   print "setCallback" 
   
button = Tk.Button(master=root, text='Set', command = setCallback)
button.pack(side=Tk.LEFT)

button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.RIGHT)

 

lists = playGame()
print lists

Tk.mainloop()



 