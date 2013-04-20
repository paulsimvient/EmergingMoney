'''
Referee File
Craig Brown, Paul Cummin, Vipin P. Veetil
CSS 610
Paper: Emergence of Money and Middlemen
'''
from __future__ import division
import math
import time
import random
import collections
import csv
from operator import itemgetter
import Agents as ag
import matplotlib.pyplot as plt	# to enable plot of histogram
import numpy as np
import constants as c

#This list will be used to keep track of goods that agents recieve...
#..though it is not their consumption goods, i.e. goods agents...
#choose to carry for purpose of indirect trade

listofMoney=[0]*(c.numOfGoods)

#agent types
types=[]

#array of all trades
allTrades=[]

#array of goods traded
goodsTraded=[]

# An agent type is defined by the set of its consumption and...
# ...production good, and the two cannot be equal

# If we have n goods, we have n(n-1) types of agents

def typesofAgents():
    for i in range(0,c.numOfGoods):
        for j in range(0, c.numOfGoods):
            if i != j:
                nlist = [str(i),str(j),str(j)]
                types.append(nlist)

typesofAgents()

# We generate agent1 list of agents

agentList = [ag.simpleAgents() for count in xrange(c.numOfAgents)]

# And we give each agents agent1 list of consumption good,..
# ...production good and carry good. Initially the production...
# ...good and carry good are the same

countType=0
for i in agentList:
    while countType<=c.numOfAgents-1:
        agentList[countType].goods=types[countType]
        countType+=1


# this function defines one round of play

def playRound(agent1,agent2):

# this function give the value for agent "agent1" of trading with agents "agent2"

    def value_trade(agent1,agent2):

# if the good "agent2" has is "agent1" consumption good then "agent1" value...
# ...from trading is utility of 1 from consumption minus cost of trade

        if agent1.goods[c.consumed_good]==agent2.goods[c.held_good]:
            tradeValue_Eat=1-(agent1.cost[int(agent2.goods[c.held_good])]+agent2.cost[int(agent1.goods[c.held_good])])/2
            tradeValue=tradeValue_Eat
            return tradeValue
        else:

#otherwise agent "agent1" computes the expected benefit from...
#... buying agent1 good it does not consume

# first the agent computes the likelihood that it will be able...
#... to trade the good it recieves from "agent2" for the good it...
# consumes next period, to do this it simply looks at how many times..
#.. the good that "agent2" has been traded in the past

            if c.memory<len(goodsTraded):
                memory_goodTraded=goodsTraded[-c.memory:]
            else:
                memory_goodTraded=goodsTraded

            past_trades=memory_goodTraded.count(agent2.goods[c.held_good])


            total_trades=len(goodsTraded)


# the agent then computes the expected cost of trading the good that..
#..."agent2" has next period, the agent simple takes the...
#..average cost from agent1 sample

            sampleList=random.sample(agentList,c.sampleSize)
            sample_costList=[]
            for i in sampleList:
                sample_costList.append(i.cost[int(agent2.goods[c.held_good])])
            sampleCost=np.mean(sample_costList)

# the agent also computes the cost of trading now

            costNow=(agent1.cost[int(agent2.goods[c.held_good])]+agent2.cost[int(agent1.goods[c.held_good])])/2
            expected_costPartner=sampleCost
            expected_costTomorrow=(agent1.cost[0]+expected_costPartner)/2

# if the good "agent2" has has never been traded before then "agent1" assigns...
#... agent1 random value for aquiring it and subtracts the cost of trading

            if  past_trades==0:
                tradeValue=random.uniform(0,1)-costNow
                return tradeValue

# if the good "agent2" has has been traded before, then agent1 computes...
#... the probability of trading it next period, computed expected...
#... cost of trading it, and also substracts cost of trading it now

            else:
                prob=past_trades/total_trades
                tradeValue_NoEat=prob*(1-expected_costTomorrow)-costNow
                tradeValue=tradeValue_NoEat
                return 1
                return tradeValue



#this function computes the value from not trading and is...
#... indentical to the part of value_trade function after else...
#... statement, except that if "agent1" does not trade now then it does...
#... not incur the cost of trading now

    def value_noTrade(agent1,agent2):

            sampleList=random.sample(agentList,c.sampleSize)
            sample_costList=[]
            for i in sampleList:
                sample_costList.append(i.cost[int(agent2.goods[c.held_good])])
            sampleCost=np.mean(sample_costList)
            expected_costPartner=sampleCost

            expected_costTomorrow=(agent1.cost[0]+expected_costPartner)/2

            past_trades=goodsTraded.count(agent1.goods[c.held_good])
            total_trades=len(goodsTraded)

            if past_trades==0:
                noTrade_value=random.uniform(0,1)
                return noTrade_value

            else:
                prob=past_trades/total_trades
                noTrade_value=prob*(1-expected_costTomorrow)
                return noTrade_value



# this function computes whether agent "agent1" prefers to trade or not ...
#...trade, it returns true if agent "agent1" prefers to trade

    def single_decision(agent1,agent2):
        if value_trade(agent1,agent2)>value_noTrade(agent1,agent2):
            return True
        return False


# this function computes whether both agents wish to trade, ...
#...it returns true if both agents wish to trade

    def final_decision(agent1,agent2):
        if single_decision(agent1,agent2)==True and single_decision(agent2,agent1)==True:
            return True
        return False


# if both agents wish to trade then we update values, store data

    if final_decision(agent1,agent2)==True:

# if the good one agnet carries is the other agents consumption good..
#.. and vice versa

        if  agent1.goods[c.consumed_good]==agent2.goods[c.held_good] and agent1.goods[c.held_good]==agent2.goods[c.consumed_good]:

#append the list of traded goods, which keeps track of couples trades

            allTrades.append((agent1.goods[c.held_good],agent2.goods[c.held_good]))

# append the list of traded goods which keeps track of...
#...individual goods traded

            goodsTraded.append(agent1.goods[c.held_good])
            goodsTraded.append(agent2.goods[c.held_good])

# agent agent1 and agent2 will update its data

            agent1.result(agent1.goods[c.consumed_good],
                          agent2.goods[c.held_good],
                          agent1.goods[c.held_good],
                          value_trade(agent1,agent2))
            
            agent2.result(agent2.goods[c.consumed_good],
                          agent1.goods[c.held_good],
                          agent2.goods[c.held_good],
                          value_trade(agent2,agent1))


        elif agent1.goods[c.consumed_good]==agent2.goods[c.held_good] and agent1.goods[c.held_good]!=agent2.goods[c.consumed_good]:
            
            allTrades.append((agent1.goods[c.held_good],
                              agent2.goods[c.held_good]))
            
            goodsTraded.append(agent1.goods[c.held_good])
            goodsTraded.append(agent2.goods[c.held_good])
            
            agent1.result(agent1.goods[c.consumed_good],
                          agent2.goods[c.held_good],
                          agent1.goods[c.held_good],
                          value_trade(agent1,agent2))
            
            agent2.result(agent1.goods[c.held_good],
                          agent1.goods[c.held_good],
                          agent2.goods[c.held_good],
                          value_trade(agent2,agent1))

# since agent "agent2" is recieving agent1 good which is not its...
#... consumption good, we call this the use of money.

            listofMoney[int(agent1.goods[c.held_good])]+=1

        elif agent1.goods[c.consumed_good]!=agent2.goods[c.held_good] and agent1.goods[c.held_good]==agent2.goods[c.consumed_good]:
            allTrades.append((agent1.goods[c.held_good],agent2.goods[c.held_good]))
            goodsTraded.append(agent1.goods[c.held_good])
            goodsTraded.append(agent2.goods[c.held_good])
            agent1.result(agent2.goods[c.held_good],agent2.goods[c.held_good],agent1.goods[c.held_good],value_trade(agent1,agent2))
            agent2.result(agent2.goods[c.consumed_good],agent1.goods[c.held_good],agent2.goods[c.held_good],value_trade(agent2,agent1))
            listofMoney[int(agent2.goods[c.held_good])]+=1

        elif agent1.goods[c.consumed_good]!=agent2.goods[c.held_good] and agent1.goods[c.held_good]!=agent2.goods[c.consumed_good]:
            allTrades.append((agent1.goods[c.held_good],agent2.goods[c.held_good]))
            goodsTraded.append(agent1.goods[c.held_good])
            goodsTraded.append(agent2.goods[c.held_good])
            agent1.result(agent2.goods[c.held_good],agent2.goods[c.held_good],agent1.goods[c.held_good],value_trade(agent1,agent2))
            agent2.result(agent1.goods[c.held_good],agent1.goods[c.held_good],agent2.goods[c.held_good],value_trade(agent2,agent1))


            listofMoney[int(agent1.goods[c.held_good])]+=1
            listofMoney[int(agent2.goods[c.held_good])]+=1



def playGame():
     for i in range(c.numofRounds):

#randomly pick two agents from the list of agents

        players=random.sample(agentList,2)
        p1=players[0]
        p2=players[1]

# ask the two players to play agent1 round of the game

        playRound(p1,p2)


playGame()

#collect data


list_goods=list(xrange(c.numOfGoods))
strList_goods=[]
for i in list_goods:
    strList_goods.append(str(i))
freq_goods=[]

for i in strList_goods:
    f=goodsTraded.count(i)
    freq_goods.append(f)


#data on money
plt.scatter(list_goods,listofMoney)
plt.title("100 Good Economy - 100,000 Rounds")
plt.xlabel("Goods")
plt.ylabel("Number of times a good is used as money")
plt.show()

 

'''
plt.scatter(list_goods,freq_goods)
plt.show()

listTrades=[]

for i in allTrades:
    g=allTrades.count(i)
    listTrades.append((i,g))

print listTrades
print allTrades
'''

