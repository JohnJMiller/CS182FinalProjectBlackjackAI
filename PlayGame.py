from BlackjackDeck import Deck
import BlackjackPlayers

#function to play a single round of blackjack
#takes a list of players and a deck object
def PlayRound(players,deck, AgentMoney,CurrentBet,in_ObservedCards,in_PastAgentState,in_PastAgentAction):
	#players is a list of players objects
	#deck is a deck object
	
	PastAgentState,PastAgentAction = in_PastAgentState,in_PastAgentAction
	ObservedCards = in_ObservedCards
	#dealer draws cards until reaching 17
	dealer_hand = BlackjackPlayers.Hand([])
	dealer_total = dealer_hand.getValue()
	
	while dealer_total < 17:
		dealer_hand.addCard(deck.draw_card())
		dealer_total = dealer_hand.getValue()

	# print "HELLO2"
	
	#dealer bust, all players win
	if dealer_total > 21:
		# print "dealer bust"
		results = []
		for player in players:
			results.append([1])
		return results, PastAgentState, PastAgentAction
		
	
	for player in players:
		player.drawCard(hand_index=0,deck=deck)
		player.drawCard(hand_index=0,deck=deck)
	
	upcard = dealer_hand.getCards()[0]
	ObservedCards.append(upcard)
	
	#this sets the play order
	rotation = list(range(len(players)))

	
	while rotation !=[]:
		for i in list(rotation):
			# print "HELLO4", i
			#take player out of rotation if they can't do anything else
			tempstate = GetGameStateOther(players,upcard,player_index=i)
			if players[i].getLegalThings(tempstate,inGame=1) == [[]] or [[],[]]:
				rotation.remove(i)
				continue
			for j in range(len(players[i].hands())):
				
				#if current player is our agent
				if i==AgentIndex:
					#get current gamestate and update weights for previous action
					GameState = GetGameStateAgent(players=players, AgentIndex=AgentIndex, current_bet=CurrentBet, total_money=AgentMoney,inGame = 1,deck = deck,ObservedCards=ObservedCards,upcard=upcard)
					players[i].update(PastAgentState,PastAgentAction,GameState, j)
					
				#if current player is not our agent
				else:
					GameState = GetGameStateOther(players = players,upcard = upcard,player_index = i)
				
				#choose and perform action
				player_action = player.getAction(hand_index = j,gamestate=GameState)
				player.performAction(action=player_action,hand_index=j,deck=deck)
				
				
				#save gamestate if this is the agent for use in next update
				if i ==AgentIndex:
					PastAgentState = GameState
					PastAgentAction = player_action
				
					#update observed cards if this is the agent and the agent hit or doubled down 
					if player_action == "Hit" or player_action =="Double Down":
						ObservedCards.append(player[AgentIndex].getHands()[j].getCards()[-1])
					

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
	return result,PastAgentState, PastAgentAction

			
			
			
def PlayGame(MaxRounds,players,AgentIndex,AgentStartingMoney):
	#initialize with a full deck
	GameDeck = Deck()
	ObservedCards = []
	
	#Initialize gamestate
	PastAgentState = GetGameStateAgent(players, AgentIndex, current_bet = 0, total_money=AgentStartingMoney, inGame=0,deck=GameDeck,ObservedCards=[],upcard='A')
	PastAgentAction = 'Initial'
	
	#this tracks the agent's money
	AgentMoney = AgentStartingMoney
	
	#we will also track the win rate
	hands_played = 0
	hands_won = 0
	hands_tied = 0

	# print "HELLO1"

	#play MaxRounds hands of blackjack
	for r in range(MaxRounds):

		#game ends if the agent has less than $1
		if AgentMoney <= 1:
			break
		
		
		#update gamestate and update weights
		GameState = GetGameStateAgent(players, AgentIndex, current_bet = 0, total_money=AgentMoney, inGame=0,deck=GameDeck,ObservedCards=ObservedCards,upcard='A')
		players[AgentIndex].update(PastAgentState,PastAgentAction,GameState, 5)
		
		#agent selects their bet
		CurrentBet = players[AgentIndex].getAction(GameState, 5) * AgentMoney
		# print "action", players[AgentIndex].getAction(GameState, 5)
		
		#game ends if the agent stops betting
		if CurrentBet == 0:
			break
		
		#shuffle deck if there are less than <= 26 cards left
		if len(GameDeck.cards_remaining()) <=26:
			GameDeck.shuffle_deck()
			ObservedCards = []
		
		#play round
		inGame = 1
		round_results, PastAgentState, PastAgentAction = PlayRound(players,GameDeck, AgentMoney,CurrentBet,ObservedCards,PastAgentState,PastAgentAction)
		
		#update observed cards - we know which cards are left in the deck
		ObservedCards = GameDeck.revealed_cards()
		
		#payout money to agent
		#double bet if the agent doubled down
		if players[AgentIndex].getDoubledDown():
			CurrentBet = 2*CurrentBet
		
		# print "round results", round_results

		for result in round_results[AgentIndex]:

			# print "HELLO3"
			#win
			if result==1:
				AgentMoney += CurrentBet
				
				hands_won+=1
				hands_played+=1
			
			#tie
			elif result == -1:
				hands_tied += 1
				hands_played += 1
			
			#lose        
			else:
				AgentMoney -= CurrentBet
				hands_played+=1
	
	TerminalState = {'Terminal':AgentMoney}
	
	WinRate = 0.
	if hands_played != 0:
		WinRate = hands_won * 1. / hands_played

	return AgentMoney, WinRate
		

def GetGameStateAgent(players, AgentIndex, current_bet, total_money, inGame,deck,ObservedCards,upcard):
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
	'A (upcard)',
	'2 (upcard)',
	'3 (upcard)',
	'4 (upcard)',
	'5 (upcard)',
	'6 (upcard)',
	'7 (upcard)',
	'8 (upcard)',
	'9 (upcard)',
	'10 (upcard)',
	'J (upcard)',
	'Q (upcard)',
	'K (upcard)',
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
	'K (2nd hand)',
	'total money (betting)',
	'A (revealed, betting)',
	'2 (revealed, betting)',
	'3 (revealed, betting)',
	'4 (revealed, betting)',
	'5 (revealed, betting)',
	'6 (revealed, betting)',
	'7 (revealed, betting)',
	'8 (revealed, betting)',
	'9 (revealed, betting)',
	'10 (revealed, betting)',
	'J (revealed, betting)',
	'Q (revealed, betting)',
	'K (revealed, betting)']
	#initialize with zeros
	for feature in FeatureList:
		GameState[feature] = 0
	
	#revealed cards
	for card in ObservedCards:
		GameState[str(card.getName()) + ' (revealed, playing)'] += 1*inGame
		GameState[str(card.getName()) + ' (revealed, betting)'] += 1*(1-inGame)
	
	#player's hand
	agent_hand = players[AgentIndex].getHands()
	
	#primary hand
	for card in agent_hand[0].getCards():
		GameState[str(card.getName()) + ' (in hand)'] += 1*inGame
	
	
	#check for secondary hand
	if len(agent_hand) == 2:
		GameState['Split hand'] += 1*inGame
		for card in agent_hand[1].getCards():
			GameState[str(card.getName()) + ' (2nd hand)'] += 1*inGame
			
	#total_money and bet
	GameState['Current Bet'] = current_bet*inGame
	GameState['Total Money (playing)'] = total_money*inGame
	GameState['total money (betting)'] = total_money*(1-inGame)
	
	#Upcard
	GameState[upcard + ' (upcard)'] += 1*inGame
	
	#REMINDER TO FILL IN HMM PART
	
	return GameState

	
def GetGameStateOther(players,upcard,player_index):
	GameState = {}
	GameState['Hand'] = players[player_index].getHands()
	GameState['Upcard'] = upcard 
	
	return GameState
	
	