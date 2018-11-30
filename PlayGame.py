from BlackjackDeck import Deck
import BlackjackPlayers

#function to play a single round of blackjack
#takes a list of players and a deck object
def PlayRound(players,deck):
    #players is a list of players objects
    #deck is a deck object
    
    
    #dealer draws cards until reaching 17
    dealer_hand = BlackjackPlayers.Hand()
    dealer_total = dealer_hand.getValue()
    
    while dealer_total < 17:
        dealer_hand.addCard(deck.draw_card())
        dealer_total = dealer_hand.getValue()
    
    #dealer bust, all players win
    if dealer_total > 21:
        return [[1]]*len(players)
    
    
    upcard = dealer_hand.getCards()[0]
    
    
    #this sets the play order
    rotation = list(range(len(players)))
    
    while rotation !=[]:
        for i in list(rotation):
            #take player out of rotation if they can't do anything else
            if players[i].GetLegalActions() == [[]] or [[],[]]:
                rotation.remove(i)
                continue
            for j in range(len(players[i].hands())):
                player.performAction(action=player.getAction(hand_index = j,gamestate=),hand_index=j,deck=deck)
    

    #assign each player a 1 if they win, and a 0 if they lose (for each of their hands)
    result = []
    
    for player in players:
        player_list = []
        for hand in player.getHands():
            if (hand.value() > dealer_total and hand.value() <= 21):
                player_list.append(1)
            elif hand.value() == dealer_total:
                player_list.append(-1)
            else:
                player_list.append(0)
        result.append(player_list)
    
    return result

            
            
            
def PlayGame(MaxRounds=100,players,AgentIndex,AgentStartingMoney=1000):
    #initialize with a full deck
    GameDeck = Deck()
    
    #this tracks the agent's money
    AgentMoney = AgentStartingMoney
    
    #play MaxRounds hands of blackjack
    for r in range(MaxRounds):
        #game ends if the agent has less than $1
        if AgentMoney < 1:
            break
        
        #agent selects their bet
        CurrentBet = players[AgentIndex].MakeBet()
        
        #game ends if the agent stops betting
        if CurrentBet == 0:
            break
        
        #shuffle deck if there are less than <= 26 cards left
        if len(GameDeck.remaining_cards) <=26:
            GameDeck.shuffle_deck()
        
        #play round
        round_results = PlayRound(players,GameDeck)
        
        #payout money to agent
        
        #double bet if the agent doubled down
        if players[AgentIndex].getDoubledDown:
            CurrentBet = 2*CurrentBet
        
        #we will also track the win rate
        hands_played = 0
        hands_won = 0
        hands_tied = 0
        
        for result in round_results[AgentIndex]:
            #win
            if result==1:
                AgentMoney += CurrentBet
                
                hands_won+=1
                hands_played+=1
            
            #tie
            elif result = -1:
                hands_tied += 1
                hands_played += 1
            
            #lose        
            else:
                AgentMoney -= CurrentBet
                hands_played+=1
                
    return AgentMoney, WinRate
        
        
    