import math, random, util
import BlackjackPlayers.py

class Agent(Player):

    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):

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
            temp += state[feature] * weights[feature, action]
        return temp
        
    def getWeights(self):
        return self.weights

    def getValue(self, state):
        """
        V(s) = max_{a in actions} Q(s,a)
        """

        maxVal = -1 * float('inf')

        # list of legal actions
        actions = self.getLegalThings(state, inGame)

        # check if at terminal state
        if len(actions) == 0:
          return 0.

        for action in actions:
          # compute q values for each action
          qVal = self.getQValue(state, action)
          if qVal > maxVal:
            maxVal = qVal

        return maxVal

    def getPolicy(self, state):
        """
        policy(s) = arg_max_{a in actions} Q(s,a)
        """

        maxVal = -1 * float('inf')
        maxAction = None

        # list of legal actions
        actions = self.getLegalThings(state, inGame)

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

    def computeActionFromQValues(self, state):
        maxVal = -1 * float('inf')
        maxAction = None

        # list of legal actions
        actions = self.getLegalThings(state, inGame)

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

    def getAction(self, state):
        legalActions = self.getLegalThings(state, inGame)

        if util.flipCoin(self.epsilon):
          return random.choice(legalActions)

        return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):

        # terminal state
        if nextState == "Done":
            print "Done"
            print self.qvals[state, action]

        difference = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        
        #self.qvals[state, action] += self.getQValue(state, action, isBet) + alpha * difference

        for feature in state:
            self.weights[feature,action] += difference

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