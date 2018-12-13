from BlackjackDeck import Deck
from BlackjackPlayers import Card, Hand, Player
import BlackjackPlayers
import HMM

#function to play a single round of blackjack
#takes a list of players and a deck object
def PlayRound(players,deck, AgentMoney,CurrentBet,in_ObservedCards,in_PastAgentState,in_PastAgentAction, AgentIndex):
	#players is a list of players objects
	#deck is a deck object
	# print "We're Playing Now"


	PastAgentState,PastAgentAction = in_PastAgentState,in_PastAgentAction
	ObservedCards = in_ObservedCards

	AgentHMM = HMM.HMM(len(players)-1)

	# before dealer draws, get state of deck
	AgentHMM.GetCardNumbers(deck)

	#dealer draws cards until reaching 17
	dealer_hand = BlackjackPlayers.Hand([])
	dealer_total = dealer_hand.getValue()
	
	while dealer_total < 17:
		dealer_hand.addCard(deck.draw_card())
		dealer_total = dealer_hand.getValue()

	#print "Dealer Hand: ", [card.getName() for card in dealer_hand.getCards()]
	#print "Dealer Total: ", dealer_total
	# print "HELLO2"
	
	#dealer bust, all players win
	if dealer_total > 21:
		# print "dealer bust"
		results = []
		for player in players:
			results.append([1])
		return results, PastAgentState, PastAgentAction, deck
		
	
	for p in range(len(players)):
		for i in range(2):
			#player.drawCard(hand_index=0,deck=deck)
			#player.drawCard(hand_index=0,deck=deck)
			card = deck.draw_card()
			players[p].getHands()[0].addCard(card)
			#print "Starting Hand: ", [card.getName() for card in player.getHands()[0].getCards()]

			# remove from deck the cards in our hand
			if p == AgentIndex:
				AgentHMM.RemoveCard(card.getName())
	
	upcard = dealer_hand.getCards()[0]
	ObservedCards.append(upcard)

	AgentHMM.SetUpcard(upcard.getName())

	AgentHMM.RemoveCard(upcard.getName())

	# normalize HMM
	AgentHMM.CardCountToProb()

	AgentHMM.InitializePrior()
	
	#this sets the play order
	rotation = list(range(len(players)))

	NoMoreMoves = []

	turn_count = 0

	while len(NoMoreMoves) < len(rotation):
		turn_count += 1
		
		for i in rotation:

			# print "HELLO4", i
			#take player out of rotation if they can't do anything else
			if i==AgentIndex:
				tempstate = GetGameStateAgent(players=players, AgentIndex=AgentIndex, current_bet=CurrentBet, total_money=AgentMoney,inGame = 1,deck = deck,ObservedCards=ObservedCards,upcard=upcard, agentHMM=AgentHMM)
			else:
				tempstate = GetGameStateOther(players = players,upcard = upcard,player_index = i)		

				#print "Player Number: ", i
				#print "Available Actions: ", players[i].getLegalThings(tempstate,inGame=1)
			if players[i].getLegalThings(tempstate,inGame=1) == []:

				NoMoreMoves.append(i)
				continue

			#print "Rotation: ", rotation
			if i in NoMoreMoves:
				continue	
			'''
			if i ==AgentIndex:
				tempstate2 = GetGameStateAgent(players=players, AgentIndex=AgentIndex, current_bet=CurrentBet, total_money=AgentMoney,inGame = 1,deck = deck,ObservedCards=ObservedCards,upcard=upcard)
			else:
				tempstate2 = GetGameStateOther(players = players,upcard = upcard,player_index = i)		
			'''
			for j in range(len(players[i].getHands())):
				#if players[i].getLegalThings(tempstate2, inGame=1)==[]:
				#	continue
			
				#if current player is our agent
				if i==AgentIndex:
					#get current gamestate and update weights for previous action
					GameState = GetGameStateAgent(players=players, AgentIndex=AgentIndex, current_bet=CurrentBet, total_money=AgentMoney,inGame = 1,deck = deck,ObservedCards=ObservedCards,upcard=upcard,agentHMM=AgentHMM)
					#print "Hand Index: ",j
					#print "Hands: ", players[i].getHands()
					players[i].update(PastAgentState,PastAgentAction,GameState, j, inGame=1)
					
				#if current player is not our agent
				else:
					GameState = GetGameStateOther(players = players,upcard = upcard,player_index = i)
				
				# check if legal actions exist
				# if players[i].getLegalThings()
				#choose and perform action
				player_action = players[i].getAction(hand_index = j,state=GameState, inGame=1)
				#print "Player action: ", player_action
				players[i].performAction(action=player_action,hand_index=j,deck=deck)
				#print i, player_action

				
				#save gamestate if this is the agent for use in next update
				if i ==AgentIndex:
					PastAgentState = GameState
					PastAgentAction = player_action
				
					#update observed cards if this is the agent and the agent hit or doubled down 
					if player_action == "Hit" or player_action =="Double Down":
						ObservedCards.append(players[AgentIndex].getHands()[j].getCards()[-1])
				else:
					if turn_count == 1:
						# update HMM for first round only
						AgentHMM.UpdateBelief(i, player_action)


	# print "HELLO5"
	#assign each player a 1 if they win, and a 0 if they lose (for each of their hands)
	result = []

	
	for player in players:
		player_list = []
		for hand in player.getHands():
			if (hand.getValue() > dealer_total and hand.getValue() <= 21):
				player_list.append(1)
			elif hand.getValue() == dealer_total:
				player_list.append(-1)
			else:
				player_list.append(0)
		result.append(player_list)
	# print "result playgame", result

	#for player in players:
	#print "Final Hand: ", [card.getName() for card in player.getHands()[0].getCards()]

	return result, PastAgentState, PastAgentAction, deck

			
			
			
def PlayGame(MaxRounds,players,AgentIndex,AgentStartingMoney):
	#initialize with a full deck
	GameDeck = Deck()
	ObservedCards = []
	
	#Initialize gamestate
	PastAgentState = GetGameStateAgent(players, AgentIndex, current_bet = 0, total_money=AgentStartingMoney, inGame=0,deck=GameDeck,ObservedCards=[],upcard=Card("A"), agentHMM=HMM.HMM(len(players)-1))
	PastAgentAction = 'Initial'
	
	#this tracks the agent's money
	AgentMoney = AgentStartingMoney
	
	#print "Agent Money: ", AgentMoney
	previousRoundEarnings = 0
	#we will also track the win rate
	hands_played = 0
	hands_won = 0
	hands_tied = 0

	# print "HELLO1"

	#play MaxRounds hands of blackjack
	for r in range(MaxRounds):
		round_no = r

		#game ends if the agent has less than $1
		if AgentMoney <= 1:
			# print "Loser"
			break
		
		
		#update gamestate and update weights
		GameState = GetGameStateAgent(players, AgentIndex, current_bet = 0, total_money=AgentMoney, inGame=0,deck=GameDeck,ObservedCards=ObservedCards,upcard=Card('A'),agentHMM=HMM.HMM(len(players)-1))
		players[AgentIndex].update(PastAgentState,PastAgentAction,GameState, 5, inGame=0,reward = previousRoundEarnings)
		
		#agent selects their bet
		CurrentBet = players[AgentIndex].getAction(GameState, 5, inGame=0) * AgentMoney
		# print "action", players[AgentIndex].getAction(GameState, 5)
		#print "current bet", CurrentBet
		
		#game ends if the agent stops betting
		if CurrentBet == 0:
			# print "Quitter"
			break
		
		#shuffle deck if there are less than <= 26 cards left
		if len(GameDeck.cards_remaining()) <=26:
			GameDeck.shuffle_deck()
			ObservedCards = []
		
		#play round
		inGame = 1
		#print "Cards Left: ", len(GameDeck.cards_remaining())
		round_results, PastAgentState, PastAgentAction, GameDeck = PlayRound(players,GameDeck, AgentMoney,CurrentBet,ObservedCards,PastAgentState,PastAgentAction, AgentIndex)
		
		#update observed cards - we know which cards are left in the deck
		ObservedCards = GameDeck.revealed_cards()
		
		#payout money to agent
		#double bet if the agent doubled down
		if players[AgentIndex].getDoubledDown():
			CurrentBet = 2*CurrentBet
		
		#reset players
		for player in players:
			player.resetPlayer()
			

		previousRoundEarnings = 0
		# print "round results", round_results

		for result in round_results[AgentIndex]:

			# print "HELLO3"
			#win
			if result==1:
				AgentMoney += CurrentBet
				previousRoundEarnings += 1
				hands_won+=1
				hands_played+=1
			
			#tie
			elif result == -1:
				hands_tied += 1
				hands_played += 1
			
			#lose		 
			else:
				AgentMoney -= CurrentBet
				previousRoundEarnings -= 1
				hands_played+=1
	
	TerminalState = {'Terminal': AgentMoney}
	# print "Previous round earnings: ", previousRoundEarnings
	players[AgentIndex].update(PastAgentState,PastAgentAction,TerminalState, 5, inGame=0,reward=previousRoundEarnings)
	
	WinRate = 0.
	if hands_played != 0:
		WinRate = hands_won * 1. / hands_played

	return AgentMoney, WinRate, round_no
		

def GetGameStateAgent(players, AgentIndex, current_bet, total_money, inGame,deck,ObservedCards,upcard, agentHMM):
	#returns a dictionary of features indexed by strings
	GameState = {}
	FeatureList = ['Current Bet',
	'Total Money (playing)',
	'A (in hand)',
	'2 (in hand)',
	'3 (in hand)',
	'4 (in hand)',
	'5 (in hand)',
	'6 (in hand)',
	'7 (in hand)',
	'8 (in hand)',
	'9 (in hand)',
	'10 (in hand)',
	'J (in hand)',
	'Q (in hand)',
	'K (in hand)',
	'A (revealed, playing)',
	'2 (revealed, playing)',
	'3 (revealed, playing)',
	'4 (revealed, playing)',
	'5 (revealed, playing)',
	'6 (revealed, playing)',
	'7 (revealed, playing)',
	'8 (revealed, playing)',
	'9 (revealed, playing)',
	'10 (revealed, playing)',
	'J (revealed, playing)',
	'Q (revealed, playing)',
	'K (revealed, playing)',
	'HMM A',
	'HMM 2',
	'HMM 3',
	'HMM 4',
	'HMM 5',
	'HMM 6',
	'HMM 7',
	'HMM 8',
	'HMM 9',
	'HMM 10',
	'HMM J',
	'HMM Q',
	'HMM K',
	'Split hand',
	'A (2nd hand)',
	'2 (2nd hand)',
	'3 (2nd hand)',
	'4 (2nd hand)',
	'5 (2nd hand)',
	'6 (2nd hand)',
	'7 (2nd hand)',
	'8 (2nd hand)',
	'9 (2nd hand)',
	'10 (2nd hand)',
	'J (2nd hand)',
	'Q (2nd hand)',
	'K (2nd hand)']
	
	FeatureList2=['total money (betting)','A (revealed, betting)','2 (revealed, betting)','3 (revealed, betting)','4 (revealed, betting)','5 (revealed, betting)','6 (revealed, betting)','7 (revealed, betting)','8 (revealed, betting)','9 (revealed, betting)','10 (revealed, betting)','J (revealed, betting)','Q (revealed, betting)','K (revealed, betting)']
	
	card_names = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
	
	#initialize with zeros - game phase
	for feature in FeatureList:
		for name in card_names:
			GameState[feature + ' (Upcard ' + name + ')'] = 0.
	
	#initialize with zeros - betting phase
	for feature in FeatureList2:
		GameState[feature] = 0
	
	upcard_name = upcard.getName()
	
	#revealed cards
	for card in ObservedCards:
		GameState[str(card.getName()) + ' (revealed, playing)' + ' (Upcard ' + upcard_name + ')'] += 1*inGame
		GameState[str(card.getName()) + ' (revealed, betting)'] += 1*(1-inGame)
	
	#player's hand
	agent_hand = players[AgentIndex].getHands()
	
	#primary hand
	for card in agent_hand[0].getCards():
		GameState[str(card.getName()) + ' (in hand)' + ' (Upcard ' + name + ')'] += 1*inGame
	
	
	#check for secondary hand
	if len(agent_hand) == 2:
		GameState['Split hand' + ' (Upcard ' + name + ')'] += 1*inGame
		for card in agent_hand[1].getCards():
			GameState[str(card.getName()) + ' (2nd hand)' + ' (Upcard ' + name + ')'] += 1*inGame
			
	
	##Upcard
	#GameState[upcard.getName() + ' (upcard)'] += 1*inGame
	
	#REMINDER TO FILL IN HMM PART
	for key, value in agentHMM.GetExpectations().items():
		GameState['HMM ' + key + ' (Upcard ' + name + ')'] += value
	
	#total_money and bet
	GameState['Current Bet'] = current_bet*inGame/total_money
	GameState['Total Money (playing)'] = 0.#total_money*inGame
	GameState['total money (betting)'] = 1. #total_money*(1-inGame)
	
	
	
	return GameState

	
def GetGameStateOther(players,upcard,player_index):
	GameState = {}
	GameState['Hand'] = players[player_index].getHands()
	GameState['Upcard'] = upcard 
	
	return GameState
	
	