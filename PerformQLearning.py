#Actually perform training
import QLearningAgent
import PlayGame
import BlackjackDeck
from BlackjackPlayers import Card, Hand, Player
from tqdm import *
import matplotlib.pyplot as plt
import util
from BasicStrategyAgent import BasicStrategyAgent

n_episodes = 20000

weights = util.Counter()
# 0.0001, 0.1, 0.000001
Q_learning_agent = QLearningAgent.Agent(alpha=.0001,epsilon = .1,gamma=0.000001)

win_rates = []
earnings = []
weight_sum = []


for i in tqdm(range(n_episodes)):
	#print '-----------------'
	#print 'NEW ITERATION'
	#print '------------------'
	PlayerList = [BasicStrategyAgent(),BasicStrategyAgent(),Q_learning_agent]
	agent_money, win_rate = PlayGame.PlayGame(MaxRounds=10,players = PlayerList,AgentIndex = 2,AgentStartingMoney=1000)
	
	#track results
	win_rates.append(win_rate)
	earnings.append(agent_money)
	weight_sum.append(Q_learning_agent.getWeights().absoluteCount())

weights = Q_learning_agent.getWeights()

plt.plot(range(n_episodes),weight_sum)
plt.title('Weight Sum: Train')
plt.xlabel('Iteration')
plt.ylabel('Sum of Absolute Value of Feature Weights')
plt.show()

plt.plot(range(n_episodes),earnings)
plt.ylim(-35000,35000)
plt.title('Ending Money: Train')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

n_episodes_test = 2000
win_rates_test = []
earnings_test = []
weight_sum_test= []

Q_learning_agent_test = QLearningAgent.Agent(weights=weights, alpha=0.,epsilon = 0.,gamma=.9)

for i in tqdm(range(n_episodes_test)):
	PlayerList = [BasicStrategyAgent(),BasicStrategyAgent(),Q_learning_agent_test]
	agent_money, win_rate = PlayGame.PlayGame(MaxRounds=5,players = PlayerList,AgentIndex = 2,AgentStartingMoney=1000)
	
	#track results
	win_rates_test.append(win_rate)
	earnings_test.append(agent_money)
	weight_sum_test.append(Q_learning_agent_test.getWeights().totalCount())
	
plt.plot(range(n_episodes_test),earnings_test)
plt.ylim(-35000,35000)
plt.title('Ending Money: Test')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

n_episodes_test = 2000
win_rates_test = []
earnings_test = []
weight_sum_test= []

Q_learning_agent_test = QLearningAgent.Agent(weights=weights, alpha=0.,epsilon = 1.,gamma=.9)

for i in tqdm(range(n_episodes_test)):
	PlayerList = [BasicStrategyAgent(),BasicStrategyAgent(),Q_learning_agent_test]
	agent_money, win_rate = PlayGame.PlayGame(MaxRounds=5,players = PlayerList,AgentIndex = 2,AgentStartingMoney=1000)
	
	#track results
	win_rates_test.append(win_rate)
	earnings_test.append(agent_money)
	weight_sum_test.append(Q_learning_agent_test.getWeights().totalCount())
	
plt.plot(range(n_episodes_test),earnings_test)
plt.ylim(-35000,35000)
plt.title('Ending Money: Random Agent')
plt.xlabel('Iteration')
plt.ylabel('Ending Money')
plt.show()

