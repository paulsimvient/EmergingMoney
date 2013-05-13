'''
Agents File
Craig Brown, Paul Cummin, Vipin P. Veetil
CSS 610
Paper: Emergence of Money and Middlemen
'''



from __future__ import division
import math
import time
import random
import collections
import constants as c
from collections import Counter

class agentBase(object):
    def __init__(self):

#each agent is defined by (1)a vector of cost of indentifying goods...
#...(2) and a vector of goods

        self.goods=[]
        self.trade_History = []
        self.utilityHistory=[]
        self.cost = []

#create a list to store the number of trades an agent does in...
#...each type of good

        self.trades=[0]*c.numOfGoods
        self.recieved=[0]*c.numOfGoods
        self.given=[0]*c.numOfGoods
        self.money=[0]*c.numOfGoods

#create a list to store the cost for each agent to be able...
#... to tell quality of goods






# cost of indentifying any given good varies across agents...,
#...and any given agent has different cost of indentifying different..
#...goods, i.e. these are necessary and sufficient conditions...
#...for emergence of money according to Brunner and Meltzer

# we model the above by initializing each agent with a...
#...random cost for each good.



# result is information that is return by the referee to the agent,...
#...the agent stores this information

    def result(self, carry, recieved, given, utility, costList, money):
        
        self.goods[c.held_good]=carry

        self.trades[int(recieved)]=+1
        self.trades[int(given)]=+1

        self.recieved[int(recieved)]=+1
        self.given[int(given)]=+1

        self.trade_History.append((recieved,given))
        self.utilityHistory.append(utility)

      
        if money!= None: 
            _money = int(money)
            _consumed = int(self.goods[c.consumed_good])
            if _money == _consumed:
                print "you blew it"
                
            self.money[_money]+=1 

class simpleAgents(agentBase):
     def __init__(self):
        agentBase.__init__(self)



