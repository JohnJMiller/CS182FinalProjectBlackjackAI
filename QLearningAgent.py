'''
The Q-Learning Agent
Alice Liu, John Miller
'''

import math, random, util
from BlackjackPlayers import Player, Hand, Card

class Agent(Player):

	def __init__(self, weights = util.Counter(), hands = [Hand([])], alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):

		self.hands = hands
		self.doubledDown = False
		self.split = False
		self.stand = False
		self.alpha = float(alpha)
		self.epsilon = float(epsilon)
		self.discount = float(gamma)
		self.numTraining = int(numTraining)
		self.weights = weights
		self.features = util.Counter()

	def getQValue(self, state, action):
		"""
		Returns the approximate Q-value of a state/action pair
		"""
	 
		weightsum = 0
		temp = 0
		for feature in state:
			temp += state[feature] * self.weights[feature, action]
			weightsum += abs(self.weights[feature, action])
		
		return temp
		
	def getWeights(self):
		"""
		Returns the Q-Learning agent's weights
		"""
		return self.weights

	def actionsWithHandIndex(self, state, hand_index, inGame):
		"""
		Gets list of legal actions given hand index
		"""

		# list of legal actions
		actions = []
		# if betting, only one list
		if hand_index == 5:
			actions = self.getLegalThings(state, 0)
		else:
			# list of legal actions for playing
			actions = self.getLegalThings(state, inGame)[hand_index]
			
		# print "actions", actions
		return actions

	def getValue(self, state, hand_index, inGame):
		"""
		Returns the approximate V-value of a state
		V(s) = max_{a in actions} Q(s,a)
		"""

		actions = self.actionsWithHandIndex(state, hand_index, inGame)

		# check if at terminal state
		if len(actions) == 0:
		  return 0.

		qlist = []

		for action in actions:
		  # compute q values for each action
		  qlist.append(self.getQValue(state, action))

		return max(qlist)

	def getPolicy(self, state, hand_index, inGame):
		"""
		Returns Q-values
		
		policy(s) = arg_max_{a in actions} Q(s,a)
		"""

		# list of legal actions
		actions = self.actionsWithHandIndex(state, hand_index, inGame)

		# check if at terminal state
		if len(actions) == 0:
		  return None
		tuplelist = []
		for action in actions:
		  # compute q values for each action
		  tuplelist.append((self.getQValue(state, action),action))
		tuplelist.sort()

		return tuplelist[-1][-1]

	def computeActionFromQValues(self, state, hand_index, inGame):
		"""
		Returns best action from Q-values
		"""
		
		# list of legal actions
		actions = self.actionsWithHandIndex(state, hand_index, inGame)

		# check if at terminal state
		if len(actions) == 0:
		  return None
		tuplelist = []
		for action in actions:
		  # compute q values for each action
		  tuplelist.append((self.getQValue(state, action),action))
		tuplelist.sort()

		return tuplelist[-1][-1]

	def getAction(self, state, hand_index, inGame):
		"""
		Performs epsilon-greedy action selection
		"""
		
		legalActions = self.actionsWithHandIndex(state, hand_index, inGame)
		if util.flipCoin(self.epsilon):
			return random.choice(legalActions)

		return self.computeActionFromQValues(state, hand_index, inGame)

	def update(self, state, action, nextState, hand_index, inGame=1, reward=1):
		"""
		Updates feature weights
		"""
		if state == "Initial":
			return

		difference = 0.

		# terminal state
		if nextState.keys()[0] == "Terminal":
			difference = (reward + self.discount * nextState["Terminal"]) - self.getQValue(state, action)
		else:
			difference = (reward + self.discount * self.getValue(nextState, hand_index, inGame)) - self.getQValue(state, action)
			
		for feature in state:
			self.weights[feature, action] += self.alpha * difference * state[feature]
