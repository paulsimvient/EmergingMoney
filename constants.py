'''
Constants File
Craig Brown, Paul Cummin, Vipin P. Veetil
CSS 610
Paper: Emergence of Money and Middlemen
'''


from __future__ import division

numOfGoods=4
import random

numOfBaseAgents=numOfGoods*(numOfGoods-1)
#numOfAgents= 100
numofRounds=1000
sampleSize=5
memory=10

consumed_good = 0
produced_good = 1
held_good = 2 

max_fixedCost= .5

countGoods_list=0

#curvature determining how quickly increase trade reduces the cost of a good
alpha=0.5

#time discount factor
beta=0.5
