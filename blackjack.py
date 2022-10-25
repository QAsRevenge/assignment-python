import random

# Empty sets for player and dealer hand to start with
player_hand = []
dealer_hand = []


class Card:
    # Constructor for Card
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        global val
        # Ace should be able to be 1 or 11
        if self.value == 1:
            val = 'Ace'
        elif self.value == 11:
            val = 'Jack'
        elif self.value == 12:
            val = 'Queen'
        elif self.value == 13:
            val = 'King'
        else:
            val = self.value
        return '{} of {}'.format(val, self.suit)


class Deck:
    # Constructor for Deck
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
            for v in range(1, 14):
                self.cards.append(Card(s, v))

    def show(self):
        for c in self.cards:
            print(c.show())


deck = Deck()
deck.show()

# py to code:
# Deck - mainly fixed, needs shuffle
# Dealer
# Dealer hand and player hands - done
# Func. to deal out cards
# def deal_a_card(turn):
#    card_to_deal = random.choice(deck_vals)
#    turn.append(card_to_deal)
#    deck_vals.remove(card_to_deal)
# Multiple players functionallity
# Check for win

