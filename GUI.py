#!/usr/bin/env python
import matplotlib
from random import *
from Tkinter import *
from EmergingMoney import *
from constants import *
from matplotlib.font_manager import FontProperties
import csv

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

#text output
log = None

#run param space
run_space = False

#swap costs if money emerges
swap_money_emerges = False

#run in real time
realTime = False

#store when money happens
moneyHappens = -1 

#legend on
legend_on = False

#money threshold
money_threshold = .65

#graph over time
graphOverTime = True
 
fontP = FontProperties()
fontP.set_size('xx-small') 
 
        
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
 
    slist.append(Indicator(master=root, label='Number of Goods', value=10, f = 0, t = 100))
    slist.append(Indicator(master=root, label='Number of Rounds (per run)', value=500000, f = 0, t = 500000))
    slist.append(Indicator(master=root, label='Memory', value=42, f = 0, t = 100))
    slist.append(Indicator(master=root, label='Alpha %', value=77, f = 0, t = 100))
    slist.append(Indicator(master=root, label='maxCost %', value=10, f = 0, t = 100))
    


def visualize():

    global em

    a.clear() 
    
    if em == None:
        return
    
    #sorted list
    goods = em.get_goods_money() 
    list_goods = goods[1]
    if sort == True:
        list_goods = copy.deepcopy(goods[1])
        list_goods.sort(reverse=True)

    if graphOverTime == False:
        a.scatter(goods[0],list_goods)
    else:
        
        #set axis
        a.set_xlabel('number trials')
        a.set_ylabel('# times good used as money')     
         
        darray = {}
        for r in range(0,c.numOfGoods):
            darray[r] = em.costList[r]
         
        l_items = []   
        for w in sorted(darray, key=darray.get, reverse=False):
            l_items.append(w)       
        
        for r in range(0, len(l_items)):
            y = [] 
            x = []
            for i in range(0, len(trades_per_interval)):
                x.append(i) 
                y.append(trades_per_interval[i][l_items[r]])
                 
            a.plot(x,y, label='%.4f' % em.costList[l_items[r]]) 
        
        #if the legend is on
        if legend_on == True:
            a.legend(loc='upper left', prop = fontP) 
         
                
    canvas.show()

 
def regcb(trial):
     
    global moneyHappens
    global money_threshold
    
    if trial % 200 == 0: 
        
        goods = em.get_goods_money() 
        list_goods = goods[1]
        
        if len(list_goods) == 0:
            return
        
        list_goods = copy.deepcopy(goods[1])
        list_goods.sort(reverse=True)
        
        #top two
        highest = list_goods[0] + list_goods[1]
        if highest > 20:
            others = 0
            for r in list_goods:
                others+=r
           
            if others != 0 and highest/(others*1.0) >= money_threshold and moneyHappens == -1:
                print "yay! money"
                index = goods[1].index(list_goods[0])
                
                #just for fun, what happens when you swap costs if it emerges
                if swap_money_emerges:
                    em.SwapCosts(index)
                
                moneyHappens = trial
                



def callback(trial):
 
    global trades_per_interval
    global graphOverTime
    
    #visualize data
    if realTime == True and trial % 500 == 0: 
        visualize()
        
    if graphOverTime == TRUE:
        goods = em.get_goods_money()  
        trades_per_interval.append(copy.deepcopy(goods[1]))
        
    #check for money
    regcb(trial)
  

  
def sortDescend():
    global sort
    sort = not sort
    visualize()

def reviewRealTime():
    global realTime
    realTime = not realTime
    visualize()
    
def rps():
    global run_space
    run_space = not run_space
    

def runParameterSpace():
    
    global em 
    global moneyHappens
    
    numGoods = int(slist[0].var.get())
    numTrials = int(slist[1].var.get())
    memory = int(slist[2].var.get()) 
    alpha = (slist[3].var.get()/100.0)
    maxCost = (slist[4].var.get()/100.0)
    
    #incrementing values
    increment = 10
    
  
    print "theshold", money_threshold, "memory, alpha, maxcost (s)"
    
    for i in range(0,100,increment): 
        for j in range(0,100,increment): 
            em = EmergingMoney(numGoods, numTrials, i, (j*.010), maxCost)
            em.register(regcb)
            moneyHappens = -1
            em.playGame()
            visualize() 
            print i, j*.010, maxCost, moneyHappens 
          
    
    print "memory, alpha, maxcost (s)"

    for i in range(0,100,increment): 
        for j in range(0,100,increment): 
            em = EmergingMoney(numGoods, numTrials, j, (i*.010), maxCost)
            em.register(regcb)
            moneyHappens = -1
            em.playGame()
            visualize()
            
            print j, i*.010, maxCost, moneyHappens  
    
 
                
    print "memory (s), alpha, maxcost"

    for i in range(0,100,increment): 
        for j in range(0,100,increment): 
            em = EmergingMoney(numGoods, numTrials, memory, (i*.010), (j*.010))
            em.register(regcb)
            moneyHappens = -1
            em.playGame()
            visualize()
            
            print memory, (i*.010), (j*.010),  moneyHappens 

    print "memory (s), alpha, maxcost"
               
    for i in range(0,100,increment): 
        for j in range(0,100,increment): 
            em = EmergingMoney(numGoods, numTrials, memory, (j*.010), (i*.010))
            em.register(regcb)
            moneyHappens = -1
            em.playGame()
            visualize()
            print memory, (j*.010), (i*.010),  moneyHappens
                
    print "memory , alpha(s), maxcost"
    
    for i in range(0,100,increment): 
        for j in range(0,100,increment): 
            em = EmergingMoney(numGoods, numTrials, i, alpha, (j*.010))
            em.register(regcb)
            moneyHappens = -1
            em.playGame()
            visualize()
            
            print i, alpha, (j*.010), moneyHappens
           
    
    print "memory , alpha(s), maxcost"
               
    for i in range(0,100,increment): 
        for j in range(0,100,increment): 
            em = EmergingMoney(numGoods, numTrials, j, alpha, i*.010)
            em.register(regcb)
            moneyHappens = -1
            em.playGame()
            visualize()
            print j, alpha, i*.010, moneyHappens
            
    print "done"
  
def swapMoney():
    global swap_money_emerges
    swap_money_emerges = not swap_money_emerges
          
def setLegend():
    global legend_on
    legend_on = not legend_on
    visualize()    
    
def run():

    global em
    global counter
    global trades_per_interval
    global moneyHappens
    
    #run param space
    if run_space == True:
        runParameterSpace()
        return

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
    moneyHappens = -1
    #set if real time true
    if realTime == True or graphOverTime == True:
        em.register(callback)

    em.playGame()
    visualize()
    
    print numGoods, numTrials, memory, alpha,maxCost, "money", moneyHappens
    
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

button = Tk.Button(master=root, text='Set', command = run)
button.pack(side=Tk.RIGHT)

canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.RIGHT)

#do real time analysis
cb = Checkbutton(master=root, text="Real Time Analysis", command = reviewRealTime)
cb.pack(side=Tk.RIGHT) 

#plot trades
cb = Checkbutton(master=root, text="Run Parameter Space", command = rps)
cb.pack(side=Tk.RIGHT)
 
#set legend
#cb = Checkbutton(master=root, text="Legend (Costs of Goods)", command = setLegend)
#cb.pack(side=Tk.TOP)
#cb.select()
#setLegend()
 
#set legend
cb = Checkbutton(master=root, text="swap costs when money emerges", command = swapMoney)
cb.pack(side=Tk.TOP) 
setLegend()

init_plot()
 
Tk.mainloop()

