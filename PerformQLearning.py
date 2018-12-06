#Actually perform training
import QLearningAgent
import PlayGame
import BlackjackDeck
import BlackjackPlayers
from tqdm import *


n_episodes = 2

Q_learning_agent = QLearningAgent.Agent(alpha=.5,epsilon = .05,gamma=1)

win_rates = []
earnings = []

for i in tqdm(range(n_episodes)):
    PlayerList = [BlackjackPlayers.Player(),BlackjackPlayers.Player(),Q_learning_agent]
    agent_money, win_rate = PlayGame.PlayGame(MaxRounds=2,players = PlayerList,AgentIndex = 2,AgentStartingMoney=1000)
    
    #track results
    win_rates.append(win_rate)
    earnings.append(agent_money)
    


