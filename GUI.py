#!/usr/bin/env python
import matplotlib
from random import *
from Tkinter import *
from EmergingMoney import *
from constants import *

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

#emerging money class
em = None

#list of things
slist = []

#get trades for each time interval
trades_per_interval = []

#sort items
sort = False

#run in real time
realTime = False

#graph over time
graphOverTime = False
 


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

    #slist.append(Indicator(master=root, label='Number Runs', value=1, f = 1, t = 1000000)) 
    slist.append(Indicator(master=root, label='Number of Goods', value=10, f = 0, t = 100))
    slist.append(Indicator(master=root, label='Number of Rounds (per run)', value=1000, f = 0, t = 1000000))
    slist.append(Indicator(master=root, label='Memory', value=10, f = 10, t = 100))
    slist.append(Indicator(master=root, label='Alpha %', value=0.5, f = 0, t = 100))
    slist.append(Indicator(master=root, label='maxCost %', value=1, f = 0, t = 100))




def visualize():

    global em

    a.clear() 
    #sorted list
    goods = em.get_goods_money() 
    list_goods = goods[1]
    if sort == True:
        list_goods = copy.deepcopy(goods[1])
        list_goods.sort(reverse=True)

    if graphOverTime == False:
        a.scatter(goods[0],list_goods)
    else:
        
         
        a.set_xlabel('number trials')
        a.set_ylabel('number trades')    
         
        darray = {}
        for r in range(0,c.numOfGoods):
            darray[r] = em.costList[r]
         
        l_items = []   
        for w in sorted(darray, key=darray.get, reverse=True):
            l_items.append(w)       
        
        for r in range(0, len(l_items)):
            y = [] 
            x = []
            for i in range(0, len(trades_per_interval)):
                x.append(i) 
                y.append(trades_per_interval[i][l_items[r]])
                 
            a.plot(x,y, label='%.4f' % em.costList[l_items[r]]) 
        
        a.legend(loc='upper left') 
         
                
    canvas.show()


counter = 0
def callback():

    global counter 
    global trades_per_interval
    global graphOverTime
    
    #visualize data
    if realTime == True:
        visualize()
        
    if graphOverTime == TRUE:
        goods = em.get_goods_money()  
        trades_per_interval.append(copy.deepcopy(goods[1]))
         

def sortDescend():
    global sort
    sort = not sort
    visualize()

def reviewRealTime():
    global realTime
    realTime = not realTime
    visualize()

def graphTime():
    global graphOverTime
    graphOverTime = not graphOverTime
    visualize()
    
def setCallback():

    global em
    global counter
    global trades_per_interval

    #reset counter
    counter = 0
    
    #reset trades
    trades_per_interval = []

    #na = c.numOfAgents, ng = c.numOfGoods, nr = c.numofRounds, ss = c.sampleSize
    numGoods = int(slist[0].var.get())
    numTrials = int(slist[1].var.get())
    memory = int(slist[2].var.get()) 
    alpha = (slist[3].var.get()/100.0)
    maxCost = (slist[4].var.get()/100.0)
     
    em = EmergingMoney( numGoods, numTrials,memory, alpha,maxCost)

    #set if real time true
    if realTime == True or graphOverTime == True:
        em.register(callback)

    em.playGame()
    visualize()
    
    goods = em.get_goods_money() 
    list_goods = goods[1]
    print list_goods
    


#do everything
root = Tk.Tk()
root.wm_title("Emergence of Money")


#figure and canvas
f = Figure(figsize=(8,3), dpi=100)
canvas = FigureCanvasTkAgg(f, master=root)
a = f.add_subplot(111)

canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

button = Tk.Button(master=root, text='Set', command = setCallback)
button.pack(side=Tk.RIGHT)

canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.RIGHT)

 
cb = Checkbutton(master=root, text="Sort Descending", command = sortDescend)
cb.pack(side=Tk.RIGHT)
#c = Checkbutton(master=root, text="Review Real Time", command = reviewRealTime)
#c.pack(side=Tk.RIGHT)
cb = Checkbutton(master=root, text="Plot trades Over Time", command = graphTime)
cb.pack(side=Tk.RIGHT)
 

init_plot()
 
Tk.mainloop()


