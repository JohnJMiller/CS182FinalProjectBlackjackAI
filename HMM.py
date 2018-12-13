#HMM
import util
import BasicStrategyAgent
import BlackjackPlayers

class HMM:
    def __init__(self,n_other_players,upcard):
        self.beliefs = []
        for i in range(n_other_players):
            self.beliefs.append(util.Counter())
        self.CardProbs = []
        self.n_other_players = n_other_players
        self.upcard = upcard
        
        charts = BasicStrategyAgent().getCharts()
        self.chart1 = charts[0]
        self.chart2 = charts[1]
        
    def GetCardProbs(self,deck):
        n_cards_remaining = len(deck.cards_remaining())
        temp_beliefs = util.Counter()
        
        card_count = util.Counter()
        
        card_names = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        for name in card_names:
            card_count[name] = deck.cards_remaining_by_name(name)
        
        card_count.normalize()
        
        self.CardProbs = card_count
    
    def InitializePrior(self):
        card_names = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        for name1 in card_names:
            for name2 in card_names:
                for i in range(self.n_other_players):
                    if name1 == name2:
                        self.beliefs[i][(name1,name2),self.upcard] += 2*self.CardProbs[name1]*self.CardProbs[name2]
                    else:
                        self.beliefs[i][(name1,name2),self.upcard] += self.CardProbs[name1]*self.CardProbs[name2]
        for i in range(n_other_players):
            self.beliefs[i].normalize()
    
    
    def UpdateBelief(self,player_index,action,hand_index):
        #NOTE: THIS IS ONLY TO BE USED ON THE FIRST PASS THROUGH ALL PLAYERS
        
        card_names = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        
        
        #NOTE: We know all players only have 2 cards at this point
        
        #update b_prime
        for name1 in card_names:
            for name2 in card_names:
                if ((name1,name2),self.upcard) in self.chart1.keys():
                    if self.chart1[((name1,name2),self.upcard)] == action:
                        continue
                    else: 
                        self.beliefs[player_index][((name1,name2),self.upcard)] = 0
                        self.beliefs[player_index][((name2,name1),self.upcard)] = 0
                elif ((name2,name1),self.upcard) in self.chart1.keys():
                    if self.chart1[((name2,name1),self.upcard)] == action:
                        continue
                    else: 
                        self.beliefs[player_index][((name1,name2),self.upcard)] = 0
                        self.beliefs[player_index][((name2,name1),self.upcard)] = 0
                else:
                    #look at value
                    hand = BlackjackPlayers.Hand([BlackjackPlayers.Card(name1),BlackjackPlayers.Card(name2)])
                    hand_value = hand.getValue()
                    if hand_value >=18:
                        if action == "Stand":
                            continue
                        else:
                            self.beliefs[player_index][((name1,name2),self.upcard)] = 0
                            self.beliefs[player_index][((name2,name1),self.upcard)] = 0
                    
                    elif self.chart2[hand_value,upcard] == action:
                        continue
                    else:
                        self.beliefs[player_index][((name1,name2),self.upcard)] = 0
                        self.beliefs[player_index][((name2,name1),self.upcard)] = 0
        self.beliefs[player_index].normalize()
    
    
    def GetExpectations(self):
        
        Expectations = util.Counter()
    
        for hand,upcard in self.beliefs.sortedKeys():
            for card in hand:
                Expectations[card] += self.beliefs[(hand,upcard)]
        
        return Expectations