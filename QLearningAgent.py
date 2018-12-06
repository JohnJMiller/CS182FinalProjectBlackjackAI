import math, random, util
from BlackjackPlayers import Player, Hand, Card

class Agent(Player):

	def __init__(self, hands = [Hand([])], alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):

		self.hands = hands
		self.doubledDown = False
		self.split = False
		self.alpha = float(alpha)
		self.epsilon = float(epsilon)
		self.discount = float(gamma)
		self.numTraining = int(numTraining)

		#self.qvals = util.Counter()
		self.weights = util.Counter()
		self.features = util.Counter()

	def getQValue(self, state, action):

		temp = 0
		for feature in state:
			temp += state[feature] * self.weights[feature, action]
		return temp
		
	def getWeights(self):
		return self.weights

	def actionsWithHandIndex(self, state, hand_index):
		'''Gets list of legal actions given hand index'''

		# list of legal actions
		actions = []
		# if betting, only one list
		if hand_index == 5:
			# print "betting, index 5"
			actions = self.getLegalThings(state, 0)
		else:
			# print "playing, hand index", hand_index
			# list of legal actions for playing
			actions = self.getLegalThings(state, inGame)[hand_index]

		# print "actions", actions
		return actions

	def getValue(self, state, hand_index):
		"""
		V(s) = max_{a in actions} Q(s,a)
		"""

		maxVal = -1 * float('inf')

		actions = self.actionsWithHandIndex(state, hand_index)

		# check if at terminal state
		if len(actions) == 0:
		  return 0.

		for action in actions:
		  # compute q values for each action
		  qVal = self.getQValue(state, action)
		  if qVal > maxVal:
			maxVal = qVal

		return maxVal

	def getPolicy(self, state, hand_index):
		"""
		policy(s) = arg_max_{a in actions} Q(s,a)
		"""

		maxVal = -1 * float('inf')
		maxAction = None

		# list of legal actions
		actions = self.actionsWithHandIndex(state, hand_index)

		# check if at terminal state
		if len(actions) == 0:
		  return None

		for action in actions:
		  # compute q values for each action
		  qVal = self.getQValue(state, action)
		  if qVal > maxVal:
			maxVal = qVal
			maxAction = action

		return maxAction

	def computeActionFromQValues(self, state, hand_index):
		maxVal = -1 * float('inf')
		maxAction = None

		# list of legal actions
		actions = self.actionsWithHandIndex(state, hand_index)

		# check if at terminal state
		if len(actions) == 0:
		  return None

		for action in actions:
		  # compute q values for each action
		  qVal = self.getQValue(state, action)
		  if qVal > maxVal:
			maxVal = qVal
			maxAction = action

		return maxAction

	def getAction(self, state, hand_index):
		legalActions = self.actionsWithHandIndex(state, hand_index)

		if util.flipCoin(self.epsilon):
			return random.choice(legalActions)

		return self.computeActionFromQValues(state, hand_index)

	def update(self, state, action, nextState, hand_index):

		if state == "Initial":
			return

		difference = 0

		# terminal state
		if nextState == "Terminal":
			difference = (self.discount * nextState["Terminal"]) - self.getQValue(state, action)
		else:
			difference = (self.discount * self.getValue(nextState, hand_index)) - self.getQValue(state, action)
		
		#self.qvals[state, action] += self.getQValue(state, action, isBet) + alpha * difference

		for feature in state:
			self.weights[feature, action] += self.alpha * difference * state[feature]

	####################################
	#    Read These Functions          #
	####################################

	# def observeTransition(self, state,action,nextState,deltaReward):
	#     """
	#         Called by environment to inform agent that a transition has
	#         been observed. This will result in a call to self.update
	#         on the same arguments

	#         NOTE: Do *not* override or call this function
	#     """
	#     self.episodeRewards += deltaReward
	#     self.update(state,action,nextState,deltaReward)

	# def startEpisode(self):
	#     """
	#       Called by environment when new episode is starting
	#     """
	#     self.lastState = None
	#     self.lastAction = None
	#     self.episodeRewards = 0.0

	# def stopEpisode(self):
	#     """
	#       Called by environment when episode is done
	#     """
	#     if self.episodesSoFar < self.numTraining:
	#         self.accumTrainRewards += self.episodeRewards
	#     else:
	#         self.accumTestRewards += self.episodeRewards
	#     self.episodesSoFar += 1
	#     if self.episodesSoFar >= self.numTraining:
	#         # Take off the training wheels
	#         self.epsilon = 0.0    # no exploration
	#         self.alpha = 0.0      # no learning

	# def isInTraining(self):
	#     return self.episodesSoFar < self.numTraining

	# def isInTesting(self):
	#     return not self.isInTraining()

	# def __init__(self, actionFn = None, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
	#     """
	#     actionFn: Function which takes a state and returns the list of legal actions

	#     alpha    - learning rate
	#     epsilon  - exploration rate
	#     gamma    - discount factor
	#     numTraining - number of training episodes, i.e. no learning after these many episodes
	#     """
	#     if actionFn == None:
	#         actionFn = lambda state: state.getLegalActions()
	#     self.actionFn = actionFn
	#     self.episodesSoFar = 0
	#     self.accumTrainRewards = 0.0
	#     self.accumTestRewards = 0.0
	#     self.numTraining = int(numTraining)
	#     self.epsilon = float(epsilon)
	#     self.alpha = float(alpha)
	#     self.discount = float(gamma)

	# ################################
	# # Controls needed for Crawler  #
	# ################################
	# def setEpsilon(self, epsilon):
	#     self.epsilon = epsilon

	# def setLearningRate(self, alpha):
	#     self.alpha = alpha

	# def setDiscount(self, discount):
	#     self.discount = discount

	# def doAction(self,state,action):
	#     """
	#         Called by inherited class when
	#         an action is taken in a state
	#     """
	#     self.lastState = state
	#     self.lastAction = action