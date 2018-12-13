#Actually perform training
import QLearningAgent
import PlayGame
import BlackjackDeck
from BlackjackPlayers import Card, Hand, Player
from tqdm import *
import matplotlib.pyplot as plt
import util
from BasicStrategyAgent import BasicStrategyAgent
import numpy as np

n_episodes = 10000
max_rounds = 10
starting_money = 1000

weights = util.Counter()
# 0.0001, 0.1, 0.000001
Q_learning_agent = QLearningAgent.Agent(alpha=.1,epsilon = .5,gamma=0.001)

win_rates = []
earnings = []
weight_sum = []
rounds = []

for i in tqdm(range(n_episodes)):
	#print '-----------------'
	#print 'NEW ITERATION'
	#print '------------------'
	PlayerList = [BasicStrategyAgent(),BasicStrategyAgent(),Q_learning_agent]
	agent_money, win_rate, no_rounds = PlayGame.PlayGame(MaxRounds=max_rounds,players = PlayerList,AgentIndex = 2,AgentStartingMoney=starting_money)
	
	#track results
	win_rates.append(win_rate)
	earnings.append(agent_money)
	weight_sum.append(Q_learning_agent.getWeights().absoluteCount())
	rounds.append(no_rounds)

cumulative_avg_earnings_train = util.CumulativeAverage(earnings)



weights = Q_learning_agent.getWeights()

plt.plot(range(n_episodes),weight_sum)
plt.title('Weight Sum: Train')
plt.xlabel('Iteration')
plt.ylabel('Sum of Absolute Value of Feature Weights')
plt.show()

plt.plot(range(n_episodes),win_rates)
plt.title('Win Rates: Train')
plt.xlabel('Iteration')
plt.ylabel('Rounds Won')
plt.show()

plt.plot(range(n_episodes),earnings)
plt.ylim(-35000,35000)
plt.title('Ending Money: Train')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

plt.plot(range(n_episodes),cumulative_avg_earnings_train)
plt.ylim(-35000,35000)
plt.title('Cumulative Avg Ending Money: Train')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()


plt.hist(rounds)
plt.title('Walking Away: Train')
plt.show()

'''
Test
'''

n_episodes_test = 1000
win_rates_test = []
earnings_test = []
weight_sum_test= []
rounds_test = []

Q_learning_agent_test = QLearningAgent.Agent(weights=weights, alpha=0.,epsilon = 0.,gamma=.9)

for i in tqdm(range(n_episodes_test)):
	PlayerList = [BasicStrategyAgent(),BasicStrategyAgent(),Q_learning_agent_test]
	agent_money, win_rate, no_rounds = PlayGame.PlayGame(MaxRounds=max_rounds,players = PlayerList,AgentIndex = 2,AgentStartingMoney=starting_money)
	
	#track results
	win_rates_test.append(win_rate)
	earnings_test.append(agent_money)
	weight_sum_test.append(Q_learning_agent_test.getWeights().totalCount())
	rounds_test.append(no_rounds)
	
plt.plot(range(n_episodes_test),earnings_test)
plt.ylim(-35000,35000)
plt.title('Ending Money: Test')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

plt.plot(range(n_episodes_test),win_rates_test)
plt.title('Win Rates: Test')
plt.xlabel('Iteration')
plt.ylabel('Rounds Won')
plt.show()

plt.hist(rounds_test)
plt.title('Walking Away: Test')
plt.show()

cumulative_avg_earnings_train_test = util.CumulativeAverage(earnings_test)
plt.plot(range(n_episodes_test),cumulative_avg_earnings_train_test)
plt.ylim(-35000,35000)
plt.title('Cumulative Avg Ending Money: Test')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

'''
Random Agent
'''

n_episodes_rand = 1000
win_rates_rand = []
earnings_rand = []
weight_sum_rand= []
rounds_rand = []

Q_learning_agent_rand = QLearningAgent.Agent(weights=weights, alpha=0.,epsilon = 1.,gamma=.9)

for i in tqdm(range(n_episodes_rand)):
	PlayerList = [BasicStrategyAgent(),BasicStrategyAgent(),Q_learning_agent_rand]
	agent_money, win_rate, no_rounds = PlayGame.PlayGame(MaxRounds=max_rounds,players = PlayerList,AgentIndex = 2,AgentStartingMoney=starting_money)
	
	#track results
	win_rates_rand.append(win_rate)
	earnings_rand.append(agent_money)
	weight_sum_rand.append(Q_learning_agent_rand.getWeights().totalCount())
	rounds_rand.append(no_rounds)
	
plt.plot(range(n_episodes_rand),earnings_rand)
plt.ylim(-35000,35000)
plt.title('Ending Money: Random Agent')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

plt.plot(range(n_episodes_rand),win_rates_rand)
plt.title('Win Rates: Random Agent')
plt.xlabel('Iteration')
plt.ylabel('Rounds Won')
plt.show()

plt.hist(rounds_rand)
plt.title('Walking Away: Random Agent')
plt.show()

cumulative_avg_earnings_train_rand = util.CumulativeAverage(earnings_rand)
plt.plot(range(n_episodes_rand),cumulative_avg_earnings_train_rand)
plt.ylim(-35000,35000)
plt.title('Cumulative Avg Ending Money: Random Agent')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

print "Mean Ending Money - Test: ", np.mean(earnings_test)
print "Mean Ending Money - Random: ", np.mean(earnings_rand)
