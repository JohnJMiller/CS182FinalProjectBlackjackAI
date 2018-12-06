#Actually perform training
import QLearningAgent
import PlayGame
import BlackjackDeck
from BlackjackPlayers import Card, Hand, Player
from tqdm import *
import matplotlib.pyplot as plt


n_episodes = 10000

Q_learning_agent = QLearningAgent.Agent(alpha=.5,epsilon = .99,gamma=1)

win_rates = []
earnings = []

for i in tqdm(range(n_episodes)):
    PlayerList = [Player([Hand([])]),Player([Hand([])]),Q_learning_agent]
    agent_money, win_rate = PlayGame.PlayGame(MaxRounds=10,players = PlayerList,AgentIndex = 2,AgentStartingMoney=1000)
    
    #track results
    win_rates.append(win_rate)
    earnings.append(agent_money)
    
plt.plot(range(10000),earnings)
plt.title('Earnings')
plt.show()
