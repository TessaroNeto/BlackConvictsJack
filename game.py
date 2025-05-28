from deck import Deck, SpecialDeck
from player import Player
import random

class Game:
    def __init__(self):
        self.deck = Deck()
        self.special_deck = SpecialDeck()
        self.player = Player("Você")
        self.bot = Player("Bot")
        self.turn = self.player
        self.round_wins = { "Você": 0, "Bot": 0 }

    def start_round(self):
        self.deck.reset()
        self.special_deck.reset()
        self.player.reset()
        self.bot.reset()
        self.turn = self.player
        self.deal_specials()

    def deal_specials(self):
        for p in [self.player, self.bot]:
            new_special = self.special_deck.draw()
            success, msg = p.add_special(new_special)
            if not success:
                print(msg)

    def next_turn(self):
        self.turn = self.bot if self.turn == self.player else self.player

    def calculate_score(self, player):
        total = 0
        used_q = False

        for card in player.hand:
            if card.label == 'Q' and not used_q:
                used_q = True
                total *= 2
            elif card.label == 'J':
                if len(player.hand) > 0:
                    removed = player.hand.pop(0)
                    self.deck.cards.append(removed)
                    random.shuffle(self.deck.cards)
            elif card.label == 'K':
                all_cards = player.hand + self.get_opponent(player).hand
                all_cards = [c for c in all_cards if c.label != 'K']
                random.shuffle(all_cards)
                mid = len(all_cards) // 2
                player.hand = all_cards[:mid]
                self.get_opponent(player).hand = all_cards[mid:]
            else:
                total += card.value
        return total

    def use_special_effect(self, player, label):
        opponent = self.get_opponent(player)

        if label.startswith("PEGUE"):
            num = int(label.split()[1])
            for card in self.deck.cards:
                if card.label == str(num):
                    player.hand.append(card)
                    self.deck.cards.remove(card)
                    return f"Pegou carta {num}"
            return f"Carta {num} não estava disponível"

        elif label == "DESCARTE ÚLTIMA":
            if player.hand:
                removed = player.hand.pop()
                return f"Descartou {removed.label}"
            return "Nenhuma carta para descartar"

        elif label == "DESCARTE MAIOR":
            if player.hand:
                highest = max(player.hand, key=lambda c: c.value if not c.is_special else -1)
                player.hand.remove(highest)
                return f"Descartou {highest.label}"
            return "Nenhuma carta válida"

        elif label == "INVERTER MÃOS":
            player.hand, opponent.hand = opponent.hand, player.hand
            return "Mãos trocadas com o oponente"

        return "Efeito desconhecido"

    def evaluate_round(self):
        player_score = self.calculate_score(self.player)
        bot_score = self.calculate_score(self.bot)

        if player_score > 21 and bot_score > 21:
            return "Empate"
        if player_score > 21:
            self.round_wins["Bot"] += 1
            return "Bot venceu"
        if bot_score > 21:
            self.round_wins["Você"] += 1
            return "Você venceu"
        if player_score == bot_score:
            return "Empate"
        if player_score > bot_score:
            self.round_wins["Você"] += 1
            return "Você venceu"
        else:
            self.round_wins["Bot"] += 1
            return "Bot venceu"

    def get_opponent(self, player):
        return self.bot if player == self.player else self.player       