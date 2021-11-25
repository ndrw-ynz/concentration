import random, os, json
from modules import card as c
import math

with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
    cards_list = json.load(f)

class Board:
    """  
    
    """
    def __init__(self, level):
        # Calculates the number of rows and cols
        num_of_cards = level*4
        num_of_pairs = num_of_cards // 2
        square = int(math.ceil(math.sqrt(num_of_cards)))
        if math.sqrt(num_of_cards) == square:
            rows = cols = square
        else:
            while num_of_cards % square != 0:
                square -= 1
            rows = square
            cols = num_of_cards // square
            if rows > cols:
                rows, cols = cols, rows

        # Formats board
        card_size = 493//rows
        spacing = (card_size%10)+10
        card_size -= spacing
        offset = {"x":(928-(spacing+card_size)*cols)//2, "y":150}
        if offset["x"] < 0:
            card_size += offset["x"]
            offset["x"] = (928-(spacing+card_size)*cols)//2
            offset["y"] = (793-(spacing+card_size)*rows)//2

        # Prepare cards
        self.cards = []
        card_keys = list(cards_list.keys())
        for _ in range(num_of_pairs):
            card_key = random.choice(card_keys)
            card_keys.remove(card_key)
            self.cards.append(c.Card(card_key))
            self.cards.append(c.Card(card_key))
        random.shuffle(self.cards)

        # Initialize format and state of cards
        i = 0
        for card in self.cards:
            current_row = i // rows
            current_col = i % rows
            x_pos = (current_row*card_size+current_row*spacing)+offset["x"]
            y_pos = (current_col*card_size+current_col*spacing)+offset["y"]
            card.size = (card_size,)*2
            card.position = (x_pos, y_pos)
            card.default_state()
            i += 1

        self.pairs_to_guess = num_of_pairs
        self.guess = None
        self.guesser = None
        self.guessing = False
        self.transition_count = 0
        self.change_scene = False
        self.preview_cards = True

    def reset_guess(self):
        self.guess = None
        self.guesser = None
        self.guessing = False

    def is_correct_guess(self):
        return self.guess.content == self.guesser.content

    def is_guesser(self, card):
        return self.guesser == card

    def is_cleared(self):
        return self.pairs_to_guess == 0

    def correct_guess(self):
        self.pairs_to_guess -= 1

    def increment_transition_count(self):
        self.transition_count += 1

    def reset_transition_count(self):
        self.transition_count = 0
