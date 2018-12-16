'''
Deck Object
John Miller, Alice Liu
'''


import random, copy
from BlackjackPlayers import Card

full_deck_strings = ['A']*4 + ['2']*4 + ['3']*4 + ['4']*4 + ['5']*4 + ['6']*4 + ['7']*4 + ['8']*4 + ['9']*4 + ['10']*4 + ['J']*4 + ['Q']*4 + ['K']*4
full_deck = []

for card in full_deck_strings:
    full_deck.append(Card(card))

random.shuffle(full_deck)

class Deck:
    def __init__(self,cards=full_deck):
        self.cards = copy.deepcopy(cards)
        random.shuffle(self.cards)
    
    def shuffle_deck(self):
        self.cards = copy.deepcopy(full_deck)
        random.shuffle(self.cards)
    
    def draw_card(self):
        return self.cards.pop()
        
    def cards_remaining(self):
        return self.cards
    
    def revealed_cards(self):
        total_deck = copy.deepcopy(full_deck)
        for card1 in self.cards_remaining():
            for card2 in total_deck:
                if card1.getName() == card2.getName():
                    total_deck.remove(card2)

        return total_deck
    
    def cards_remaining_by_name(self, name):
        n = 0
        for card in self.cards_remaining():
            if card.getName() == name:
                n += 1
        return n