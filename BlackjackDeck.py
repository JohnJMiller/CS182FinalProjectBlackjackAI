#Deck object
import random

full_deck = ['A']*4 + ['2']*4 + ['3']*4 + ['4']*4 + ['5']*4 + ['6']*4 + ['7']*4 + ['8']*4 + ['9']*4 + ['10']*4 + ['J']*4 + ['Q']*4 + ['K']*4
random.shuffle(full_deck)

class Deck:
    def __init__(self):
        self.cards = full_deck
    
    def shuffle_deck(self):
        self.cards = full_deck
        random.shuffle(self.cards)
    
    def draw_card(self):
        return self.card.pop(0)
        
    def cards_remaining(self):
        return self.cards