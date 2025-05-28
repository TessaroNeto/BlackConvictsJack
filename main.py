import pygame
import random
from config import *
from game import Game
from menu import Menu

# Inicialização
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mesa dos Condenados")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 40)

# Variáveis do jogo
game = Game()
menu = Menu(screen, font)
game.start_round()
msg_log = ""
game_state = "jogando"

game_state = "menu"
selected_character_img = None

bot_wait_start_time = 0
round_result_time = 0
winner_final = None

# Funções visuais
def draw_text(text, x, y, size="normal", color=FONT_COLOR):
    f = big_font if size == "big" else font
    img = f.render(text, True, color)
    screen.blit(img, (x, y))

def draw_hand(player, y_pos):
    for i, card in enumerate(player.hand):
        x = 100 + i * (CARD_WIDTH + 10)
        pygame.draw.rect(screen, (100, 100, 100), (x, y_pos, CARD_WIDTH, CARD_HEIGHT))
        draw_text(card.label, x + 25, y_pos + 40)

def draw_specials(player, y_pos):
    draw_text("Especiais:", 900, y_pos)
    for i, label in enumerate(player.specials):
        draw_text(f"{i+1}: {label}", 900, y_pos + 30 + i*30)

def draw_bot_cards(bot):
    x = 100
    for i in range(len(bot.hand)):
        pygame.draw.rect(screen, (50, 50, 50), (x + i * (CARD_WIDTH + 10), 150, CARD_WIDTH, CARD_HEIGHT))
        draw_text("?", x + i * (CARD_WIDTH + 10) + 25, 190)

# Loop principal
running = True
while running:
    screen.fill(BG_COLOR)

    # Eventos do usuário
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "jogando":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and not game.turn.passed:
                    game.turn.draw_card(game.deck)
                    msg_log = f"{game.turn.name} comprou uma carta."
                    game.next_turn()

                elif event.key == pygame.K_p:
                    game.turn.passed = True
                    msg_log = f"{game.turn.name} passou."
                    game.next_turn()

                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    idx = event.key - pygame.K_1
                    if idx < len(game.player.specials) and game.turn == game.player:
                        label = game.player.specials[idx]
                        used, name = game.player.use_special(label)
                        if used:
                            msg_log = game.use_special_effect(game.player, name)
                            game.next_turn()
                        else:
                            msg_log = name

    # ======== ESTADO: Jogando turno normal =========
    if game_state == "jogando":
        if game.player.passed and game.bot.passed:
            msg_log = game.evaluate_round()
            round_result_time = pygame.time.get_ticks()
            game_state = "fim_rodada"
        elif game.turn == game.bot and not game.bot.passed:
            bot_wait_start_time = pygame.time.get_ticks()
            game_state = "espera_bot"

    # ======== ESTADO: Esperando bot (cooldown) ========
    elif game_state == "espera_bot":
        elapsed = pygame.time.get_ticks() - bot_wait_start_time
        if elapsed >= 5000:
            bot_score = game.calculate_score(game.bot)
            used_special = False

            for label in game.bot.specials:
                if "PEGUE" in label:
                    num = int(label.split()[1])
                    if not any(c.label == str(num) for c in game.bot.hand):
                        used, _ = game.bot.use_special(label)
                        if used:
                            msg_log = f"Bot usou {label}"
                            game.use_special_effect(game.bot, label)
                            used_special = True
                            break
                elif label == "DESCARTE MAIOR" and bot_score > 19:
                    used, _ = game.bot.use_special(label)
                    if used:
                        msg_log = f"Bot usou {label}"
                        game.use_special_effect(game.bot, label)
                        used_special = True
                        break
                elif label == "INVERTER MÃOS" and game.calculate_score(game.player) > bot_score + 5:
                    used, _ = game.bot.use_special(label)
                    if used:
                        msg_log = f"Bot usou {label}"
                        game.use_special_effect(game.bot, label)
                        used_special = True
                        break

            if not used_special:
                if bot_score >= 19:
                    if random.random() < 0.9:
                        game.bot.passed = True
                        msg_log = "Bot passou."
                    else:
                        game.bot.draw_card(game.deck)
                        msg_log = "Bot arriscou e comprou uma carta."
                else:
                    game.bot.draw_card(game.deck)
                    msg_log = "Bot comprou uma carta."

            game.next_turn()
            game_state = "jogando"

    # ======== ESTADO: Fim de Rodada ========
    elif game_state == "fim_rodada":
        elapsed = pygame.time.get_ticks() - round_result_time
        if elapsed >= 3000:
            if game.round_wins["Você"] >= 5 or game.round_wins["Bot"] >= 5:
                winner_final = "Você" if game.round_wins["Você"] >= 5 else "Bot"
                game_state = "fim_jogo"
            else:
                game.start_round()
                msg_log = "Nova rodada iniciada!"
                game_state = "jogando"

    # ======== ESTADO: Fim de Jogo (5 vitórias) ========
    elif game_state == "fim_jogo":
        draw_text(f"{winner_final} venceu o jogo!", 400, 300, "big")
        draw_text("Pressione [R] para jogar novamente", 380, 360)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Game()
                    game.start_round()
                    msg_log = ""
                    game_state = "jogando"

    # ======== Renderização geral =========
    def draw_character_image():
     if selected_character_img:
        img = pygame.transform.scale(selected_character_img, (150, 150))
        screen.blit(img, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 170))
        
    draw_text("Mesa dos Condenados", 450, 20, "big")
    if game_state != "fim_jogo":
        draw_text(f"{game.turn.name} é o próximo", 50, 70)
        draw_text(f"[C] Comprar  [P] Passar | [1-3] Usar Especial", 50, 100)

        draw_bot_cards(game.bot)
        draw_text("Bot", 50, 130)
        draw_text("Você", 50, 520)
        draw_hand(game.player, 550)
        draw_specials(game.player, 400)

        draw_text(msg_log, 50, 650)
        draw_text(f"Vitórias → Você: {game.round_wins['Você']} | Bot: {game.round_wins['Bot']}", 900, 50)

    if game_state == "menu":
        menu.draw_main_menu()
    elif game_state == "select":
        menu.draw_character_select()
    elif game_state == "play":
        draw_text("Sua Mão:", 50, 50)
        for idx, card in enumerate(game.player.hand):
            draw_text(card.label, 50 + idx * 60, 100)
        draw_text(f"Bot tem {len(game.bot.hand)} carta(s)", 50, 200)
        draw_text(f"Vitórias: Você {game.round_wins['Você']} | Bot {game.round_wins['Bot']}", 50, 300)
        draw_text("Teclas: [C] Comprar  [P] Passar  [R] Reiniciar Rodada", 50, 600)
        draw_character_image()    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()