
import random

class Card:
    def __init__(self, label, value, is_special=False):
        self.label = label
        self.value = value
        self.is_special = is_special

    def __str__(self):
        return self.label

class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        for i in range(1, 11):
            self.cards.append(Card(str(i), i))
        self.cards.append(Card('Q', 0, is_special=True))
        self.cards.append(Card('J', 0, is_special=True))
        self.cards.append(Card('K', 0, is_special=True))
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

class SpecialDeck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = [
            "PEGUE 1", "PEGUE 2", "PEGUE 3", "PEGUE 4", "PEGUE 7", "PEGUE 8", "PEGUE 10",
            "DESCARTE ÚLTIMA", "DESCARTE MAIOR", "INVERTER MÃOS"
        ]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None