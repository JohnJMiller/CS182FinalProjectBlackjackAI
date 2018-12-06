import sys
import random

''' Global Variables'''
LIMIT = 26

class Card(object):
	def __init__(self, name):
		self.name = name

	def getName(self):
		return self.name

	def value(self):
		valdict = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
		return valdict[self.name]


class Hand(object):
	'''A list of cards that a player has at a given time'''

	def __init__(self, cards):
		# List of cards
		self.cards = cards
		self.value = 0
		self.num_cards = 0

		self.num_aces = 0
		# Number of aces
		for card in self.cards:
			if card.getName() == "A":
				self.num_aces += 1

		# At init, all aces are soft
		self.num_soft_aces = self.num_aces

	def getCards(self):
		return self.cards

	# Value of hand is an int
	def updateValue(self):
		for card in self.cards:
			self.value += card.value()

		# Bring in the aces if we go over 21
		while self.value > 21 and self.num_soft_aces > 0:
			self.value -= 10
			self.num_soft_aces -= 1

	def getValue(self):
		return self.value

	# Split the hand
	def split(self):
		self.cards = [self.cards[0]]
		return Hand([self.cards[0]])

	# Add a card to the specified hand and update value
	def addCard(self, card):
		self.cards.append(card)
		self.updateValue()

	# Number of cards in the hand
	def size(self):
		return len(self.cards)

class Player(object):
	'''The card player; agent inherits this class'''

	def __init__(self, hands = [Hand([])]):
		# A list of hands
		self.hands = hands
		self.doubledDown = False
		self.split = False

	def getHands(self):
		return self.hands

	def drawCard(self, hand_index, deck):
		self.hands[hand_index].addCard(deck.draw_card())

	def splittableHand(self):
		# Splittable if (1) one hand, (2) hand has 2 cards (3) which are identical
		return len(self.hands) == 1 and len(self.hands[0].cards) == 2 and (self.hands[0].cards)[0] == (self.hands[0].cards)[1]

	def splitHand(self):
		self.hands.append((self.hands[0]).split())
		self.split = True

	def getLegalActions(self):
		total_actions = []
		for hand in self.hands:
			# Temporary list of legal actions
			actions = []

			# If over 21, then bust
			if hand.getValue() > LIMIT:
				continue

			if hand.getValue() < LIMIT:
				actions.append("Stand")

				# Before we continue: if already doubled down, can only stand
				if self.doubledDown:
					continue

				# Otherwise, can also hit
				actions.append("Hit")

				# Can double down if hand size is 2, but can't double down if split
				if hand.size() == 2 and not self.split:
					actions.append("Double Down")

				# Splittable depending on set guidelines
				if self.splittableHand():
					actions.append("Split")

			total_actions.append(actions)

	def getLegalThings(self, state, inGame):

		if inGame:
			return self.getLegalActions()
        
        # get legal bets
		else:
			money = state['total money (betting)']
			if money <= 1.:
				return [0.]
			else:
				return [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]




	def getDoubledDown(self):
		return self.doubledDown

	def setDoubledDown(self, doubled):
		self.doubledDown = doubled 

	def performAction(self, action, hand_index, deck):
		# If we stand, nothing happens
		if action == "Hit" or action == "Double Down":
			self.draw_card(hand_index, deck)
		if action == "Split":
			self.splitHand()





