'''
A,B; B,A version
Referee File
Craig Brown, Paul Cummin, Vipin P. Veetil
CSS 610
Paper: Emergence of Money and Middlemen
'''
from __future__ import division
import math
import time
import random
from random import choice
import collections
import csv
from operator import itemgetter
import Agents as ag
import matplotlib.pyplot as plt    # to enable plot of histogram
import numpy as np
import constants as c
import Tkinter
import copy

class EmergingMoney():

    def __init__(self, ng = c.numOfGoods, nr = c.numofRounds, mem = c.memory, al=c.alpha, maxCost=c.max_fixedCost):

        #This list will be used to keep track of goods that agents recieve...
        #..though it is not their consumption goods, i.e. goods agents...
        #choose to carry for purpose of indirect trade

        c.numOfBaseAgents = ng*(ng-1) 
        c.numOfGoods = ng
        c.numofRounds = nr
        c.memory=mem
        c.alpha = al
        c.max_fixedCost = maxCost

        self.listofMoney=[0]*(c.numOfGoods)

        #agent self.types
        self.types=[]

        #array of all trades
        self.allTrades=[]

        #array of goods traded
        self.goodsTraded=[]

        #cost list
        self.costList_unchanging=[]
         

        # create a dictionary to store the cost of trading goods, the structure will be of the following kind
        # {(0,1):[0.1,0.02,0.5],(0,2):[0.1,0.6,0.02],(1,0):[0.5,0.3]}
        # (0,1) records the cost of the agent who recieved 0
        # we initialize an empty dictionary with the intention of filling it up with the above
        self.tradeCosts=dict()

        # create two list of number of goods
        self.goods_listOne=[i for i in range(c.numOfGoods)]
        self.goods_listTwo=[i for i in range(c.numOfGoods)]

        # create a list of combinations of goods, it will look like this: [(0,1),(0,2),(1,0) and so on]
        self.goodsCombinations=[]

        for i in self.goods_listOne:
            for j in self.goods_listTwo:
                self.goodsCombinations.append((i,j))

        # attaches an empty list to a dictionary where elements shows combinations of goods, so we get {(0,1):[],(0,2):[],(1,0):[]}
        for x in self.goodsCombinations:
            self.tradeCosts[x]=list()


        #print "fixed costs", c.max_fixedCost
        
        #list of costs assigned to each agent
        for i in range(0, c.numOfGoods):
            self.costList_unchanging.append(random.uniform(0,c.max_fixedCost))

   
        self.costList= copy.deepcopy(self.costList_unchanging)

                
        
         # We generate a list of agents
        self.agentList = [ag.simpleAgents() for count in xrange(c.numOfBaseAgents)]

        self.listofMoney=[0]*(c.numOfGoods)

        #initialize agent self.types
        for i in range(0,c.numOfGoods):
            for j in range(0, c.numOfGoods):
                if i != j:
                    nlist = [str(i),str(j),str(j)]
                    self.types.append(nlist)

        # And we give each agents agent1 list of consumption good,..
        # ...production good and carry good. Initially the production...
        # ...good and carry good are the same
        
        for i in range(0, len(self.types)):
            self.agentList[i].goods= self.types[i]

        for i in self.agentList:
            i.cost = self.costList
            
        #print "costs", self.costList

        #register callback funciton if necessary
        self.callback_function = None

    #store callback function
    def register(self,cb):
        self.callback_function = cb

    def callback(self, var):
        if self.callback_function != None:
            self.callback_function(var)

    # this function defines one round of play
    def playRound(self, agent1, agent2):


        # records the memory of past trades the agent has. The agents look at all combinations of past trades, record the last n she remembers
        def mem_pastTrades():
            if c.memory<len(self.allTrades):
                memory_goodTraded=self.allTrades[-c.memory:]
                return memory_goodTraded
            else:
                memory_goodTraded=self.allTrades
                return memory_goodTraded

        # records the length of past trades the agent remembers, if total trade is less than agent memory then the length is total trades
        def length_pastTrades():
            if c.memory<len(self.allTrades):
                mem_length=c.memory
                #print mem_length
                return mem_length
            else:
                mem_length=len(self.allTrades)
                return mem_length


        #compute the probability of being able to trade good agent 1 consumption good for agent 2's carry good next period.
        #This is relevant because if agent 1 trades with agent 2 then agent 2's carry goods becomes agent 1's carry good
        def ProbTradingNext(agent1,agent2):
            
            a=mem_pastTrades()
            b=length_pastTrades()

            past_tradesOne=a.count((agent2.goods[c.held_good],agent1.goods[c.consumed_good]))
            past_tradesTwo=a.count((agent1.goods[c.consumed_good],agent2.goods[c.held_good]))
            PastTrades=past_tradesOne+past_tradesTwo

            if b<c.memory:
                return random.uniform(0,1)
            else:
                #this shouldn't hapen
                if b==0:
                    return 0
                    
                prob_tradeNextPeriod=PastTrades/b
                return prob_tradeNextPeriod
 
        #compute the cost of trading agent 1's consumption good for agent 2's carry good next period.
        #This is relevant because if agent 1 trades with agent 2 then agent 2's carry goods becomes agent 1's carry good

        def unconditional_CostTradingNext(agent1,agent2):
            
            avg_pastCosts = 0
            
            #Paul Note: I don't understand this. what is c.memory>len(...)?
            if c.memory>len(self.tradeCosts):
                avg_pastCosts=random.uniform(0,(c.max_fixedCost))

            else:
                pastCosts=self.tradeCosts[int(agent1.goods[c.consumed_good]),(int(agent2.goods[c.held_good]))]
                memory_of_pastCosts=pastCosts[-c.memory:]
                
                #the problem with this is that does this is this really an effective way 
                past_costs = len(memory_of_pastCosts)
                if past_costs < 0 or len(memory_of_pastCosts) == 0:
                    avg_pastCosts=random.uniform(0,(c.max_fixedCost))
                else:
                    avg_pastCosts=np.mean(memory_of_pastCosts)
            
            expected_costPartner=avg_pastCosts
            expected_costTomorrow=(agent1.cost[int(c.consumed_good)]+expected_costPartner)/2
            return expected_costTomorrow

        # compute costs conditional on trading and not trading
        def CostTradingNext(agent1,agent2,trade_thisPeriod):
            if trade_thisPeriod==True:
                a=unconditional_CostTradingNext(agent1,agent2)
                return a
            else:
                #why agent1 and agent1?
                a=unconditional_CostTradingNext(agent1,agent1)
                return a

        # compute the cost of trading now
        def CostNow(agent1,agent2):
            a1 = int(agent2.goods[c.held_good])
            a2 = int(agent1.goods[c.held_good])
            costNow=(agent1.cost[a1]+agent2.cost[a2])/2
            return costNow

        # compute the value from trading
        def value_trade(agent1,agent2):

            #if good that I want to consume is good partner has
            if agent1.goods[c.consumed_good]==agent2.goods[c.held_good]:
                tradeValue=1-CostNow(agent1,agent2)
                return tradeValue
            else: 
                prob=ProbTradingNext(agent1,agent2)
                val=1-CostTradingNext(agent1,agent2,True)
                
                #time discount factor
                prob_val = (prob*val)
            
                tradeValue= prob_val-CostNow(agent1,agent2)
                return tradeValue
                

        # compute value from not trading
        def value_noTrade(agent1,agent2):
            
            prob=ProbTradingNext(agent1,agent1)
            val=1-CostTradingNext(agent1,agent2,False)
            
            #time discount factor
            prob_val = (prob*val)
            No_tradeValue=prob_val
           
            return No_tradeValue


        # find the decision of any one agent
        def agent_wants_to_trade_decision(agent1,agent2):
            
            v_trade = value_trade(agent1,agent2)
            v_no_trade = value_noTrade(agent1,agent2)
            
            if v_trade>v_no_trade and v_trade>0:
                return True
          
            return False


        # this function computes whether both agents wish to trade, ...
        #...it returns true if both agents wish to trade
        def both_agents_want_to_trade(agent1,agent2):
            
            trade_info1 = agent_wants_to_trade_decision(agent1,agent2)
            trade_info2 = agent_wants_to_trade_decision(agent2,agent1)
            if trade_info1==True and trade_info2==True:
                return True
            
            return False
        
        


        def record_Outcomes(agent1,agent2):


            a1_produce = agent1.goods[c.produced_good]
            a1_consumed = agent1.goods[c.consumed_good]
            a1_held = agent1.goods[c.held_good]

            a2_produce = agent2.goods[c.produced_good]
            a2_consumed = agent2.goods[c.consumed_good]
            a2_held = agent2.goods[c.held_good]
 
            if both_agents_want_to_trade(agent1,agent2)==True:
                utility_now = 1-CostNow(agent1, agent2)
                
                #append the list of traded goods, which keeps track of couples trades
                self.allTrades.append((a1_held ,a2_held)) 
                
                                    # append the list of traded goods which keeps track of...
                
                                    #...individual goods traded
                self.goodsTraded.append(a1_held)
                self.goodsTraded.append(a2_held)
                                    
                # if the good one agent carries is the other agents consumption good..
                #.. and vice versa
                #print 'first', self.costList
                
                a1_numberofTrades=self.goodsTraded.count(int(a1_held))
                a2_numberofTrades=self.goodsTraded.count(int(a2_held))
                
                
                a1_oldCost=self.costList_unchanging[int(a1_held)]
                a2_oldCost=self.costList_unchanging[int(a2_held)]
                
               
                
                a1_constantCost=a1_oldCost/2.0
                a1_variableCost=a1_oldCost/(2.0*(a1_numberofTrades**c.alpha+1))
             
                a1_newCost=a1_constantCost+a1_variableCost
                
                
               

                a2_constantCost=a2_oldCost/2.0
                a2_variableCost=a2_oldCost/(2.0*(a2_numberofTrades**c.alpha+1))
                
                a2_newCost=a2_constantCost+a2_variableCost
                
                                     
                self.costList[int(a1_held)]=a1_newCost
                self.costList[int(a2_held)]=a2_newCost
                
              
                #for i in self.agentList:
                    #i.cost=self.costList
                    


                if  a1_consumed==a2_held and a1_held ==a2_consumed:
                    
                    


                    # agent agent1 and agent2 will update its data

                    agent1.result(a1_produce ,
                                  a2_held,
                                  a1_held,
                                  utility_now,
                                  self.costList,None) 

                    agent2.result(a2_produce ,
                                  a1_held,
                                  a2_held,
                                  utility_now,
                                  self.costList,None) 

                    self.tradeCosts[(int(a1_consumed),int(a2_consumed))].append(agent1.cost[int(a1_consumed)])
                    self.tradeCosts[(int(a2_consumed),int(a1_consumed))].append(agent2.cost[int(a2_consumed)])

                #agent1 gets his consumption good but agent 2 does not

                elif a1_consumed==a2_held and a1_held !=a2_consumed:

                    

                    agent1.result(a1_produce ,
                                  a2_held,
                                  a1_held,
                                  utility_now,
                                  self.costList,None) 

                    agent2.result(a1_held,
                                  a1_held,
                                  a2_held,
                                  0,
                                  self.costList,a1_held )


                    # since agent "agent2" is recieving agent1 good which is not its...
                    #... consumption good, we call this the use of money.


                    self.listofMoney[int(a1_held )]+=1
                    self.tradeCosts[(int(a1_consumed),int(a2_consumed))].append(agent1.cost[int(a1_consumed)])
                    self.tradeCosts[(int(a2_consumed),int(a1_consumed))].append(agent2.cost[int(a2_held)])

                    #agent 2 gets consumption good but agent 1 does not

                elif a1_consumed!=a2_held and a1_held ==a2_consumed:
                   



                    agent1.result(a2_held,
                                  a2_held,
                                  a1_held,
                                  0,
                                  self.costList,a2_held)



                    agent2.result(a2_produce ,
                                  a1_held,
                                  a2_held,
                                  utility_now,
                                  self.costList,None)



                    self.listofMoney[int(a2_held)]+=1
                    self.tradeCosts[(int(a1_consumed),int(a2_consumed))].append(agent1.cost[int(a1_held )])
                    self.tradeCosts[(int(a2_consumed),int(a1_consumed))].append(agent2.cost[int(a2_consumed)])

                # neither gets consumption good

                elif a1_consumed!=a2_held and a1_held !=a2_consumed:

                   
                    agent1.result(a2_held,
                                  a2_held,
                                  a1_held,
                                  0,
                                  self.costList,a2_held) 
                    
                    agent2.result(a1_held,
                                  a1_held,
                                  a2_held,
                                  0,
                                  self.costList,a1_held )

                    self.listofMoney[int(a1_held )]+=1
                    self.listofMoney[int(a2_held)]+=1


                    self.tradeCosts[(int(a1_consumed),int(a2_consumed))].append(agent1.cost[int(a1_held )])
                    self.tradeCosts[(int(a2_consumed),int(a1_consumed))].append(agent2.cost[int(a2_held)])





        # if both agents wish to trade then we update values, store data

        record_Outcomes(agent1,agent2)
       
       

    def playGame(self):

        for i in range(c.numofRounds):

            #randomly pick two agents from the list of agents
            players=random.sample(self.agentList,2)

            p1=players[0]
            p2=players[1]

            # ask the two players to play agent1 round of the game
            self.playRound(p1,p2)

            #callback function if necessary
            self.callback(i)
            
        #print "agent 1 cost end", self.agentList[0].cost
       # print "trade costs end", self.tradeCosts
         
         
        #print "individual money endand size", len(self.agentList)
       # for i in self.agentList:
           # print i.money, i.goods


    def get_goods_money(self):
        #collect data
        list_goods=list(xrange(c.numOfGoods))
        strList_goods=[]
        for i in list_goods:
            strList_goods.append(str(i))
        freq_goods=[]

        for i in strList_goods:
            f=self.goodsTraded.count(i)
            freq_goods.append(f)

        return list_goods, self.listofMoney

    def plot(self):

        goods = self.get_goods_money()

        plt.scatter(goods[0],goods[1])

        buf = "%d Good Economy - %d rounds" % (c.numOfGoods, c.numofRounds)
        plt.title(buf)
        plt.xlabel("Goods")
        plt.ylabel("Number of times a good is used as money")
        plt.show()


def run():
     
    em = EmergingMoney()
    em.playGame()
    em.plot()


 