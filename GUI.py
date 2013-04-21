#!/usr/bin/env python
import matplotlib
from random import *
from Tkinter import *
from EmergingMoney import *
import copy

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

em = None
slist = []
sort = False
   
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
  
  
 
def init_plot():        
    
    # a tk.DrawingArea
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    #toolbar = NavigationToolbar2TkAgg( canvas, root )
    #toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
     
  
    slist.append(Indicator(master=root, label='Number of Agents', value=500, f = 0, t = 1000)) 
    slist.append(Indicator(master=root, label='Number of Goods', value=5, f = 0, t = 100)) 
    slist.append(Indicator(master=root, label='Number of Rounds', value=1000, f = 0, t = 10000)) 
    slist.append(Indicator(master=root, label='Sample Size', value=5, f = 0, t = 100)) 
   
 
def visualize():
   
    global em
    
    a.clear()
    
    #a.plot(t,s)
    a.set_title('Emergence of Money')
    a.set_xlabel('Goods')
    a.set_ylabel('Goods Used As Money')
 
    goods = em.get_goods_money()
    
    #sorted list
    list_goods = copy.deepcopy(goods[1])
    if sort == True:
        list_goods.sort(reverse=True)
     
    a.scatter(goods[0],list_goods)    
    canvas.show()
    

def sortAscend():
    
    global sort
    sort = not sort
    visualize()
     
 
def setCallback():
    
    global em
    
    #na = c.numOfAgents, ng = c.numOfGoods, nr = c.numofRounds, ss = c.sampleSize
    v_0 = int(slist[0].var.get())
    v_1 = int(slist[1].var.get())
    v_2 = int(slist[2].var.get())
    v_3 = int(slist[3].var.get())    
    em = EmergingMoney(v_0, v_1, v_2, v_3)    
    em.playGame()    
    visualize()
   

#do everything
root = Tk.Tk()
root.wm_title("Emergence of Money")    

#figure and canvas
f = Figure(figsize=(6,5), dpi=100)
canvas = FigureCanvasTkAgg(f, master=root) 
a = f.add_subplot(111)
 
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

button = Tk.Button(master=root, text='Set', command = setCallback)
button.pack(side=Tk.RIGHT)
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)    
button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.RIGHT)   

c = Checkbutton(master=root, text="Sort Descending", command = sortAscend)
c.pack(side=Tk.RIGHT)


init_plot()

em = EmergingMoney()
em.playGame()
visualize()
  
Tk.mainloop()


