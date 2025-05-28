class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.specials = []
        self.score = 0
        self.passed = False
        self.discard_pile = []

    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card

    def add_special(self, card_label):
        if card_label not in self.specials:
            if len(self.specials) < 3:
                self.specials.append(card_label)
                return True, ""
            else:
                return False, f"Carta especial '{card_label}' descartada (máximo atingido)"
        else:
            return False, f"Carta especial '{card_label}' já existe (descartada)"

    def use_special(self, label):
        if label not in self.specials:
            return False, "Carta especial não disponível"
        self.specials.remove(label)
        return True, label

    def reset(self):
        self.hand = []
        self.passed = False
        self.score = 0  