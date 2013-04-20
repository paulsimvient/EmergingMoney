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

#create a list to store the number of trades an agent does in...
#...each type of good

        self.trades=[0]*c.numOfGoods

#create a list to store the cost for each agent to be able...
#... to tell quality of goods

        self.cost = []

# cost of indentifying any given good varies across agents...,
#...and any given agent has different cost of indentifying different..
#...goods, i.e. these are necessary and sufficient conditions...
#...for emergence of money according to Brunner and Meltzer

# we model the above by initializing each agent with a...
#...random cost for each good.


# the random cost has two components, a fixed cost which is...
#...drawn from a uniform(0,maxFixedCost) and a variable cost which...
#...depends on number of time an agent has traded in a particular good

        countCost=0
        while countCost<=c.numOfGoods-1:
            self.cost.append(random.uniform(0,c.max_fixedCost)+
                random.uniform(0,1)/((1+self.trades[countCost])*2))
            countCost+=1

# result is information that is return by the referee to the agent,...
#...the agent stores this information

    def result(self,carry,recieved,given,utility):
        self.goods[c.held_good]=carry
        self.trade_History.append((recieved,given))
        self.utilityHistory.append(utility)

# when an agent recieves or gives a good, it recordes it as a trade

        self.trades[int(recieved)]+=1
        self.trades[int(given)]+=1


class simpleAgents(agentBase):
     def __init__(self):
        agentBase.__init__(self)




