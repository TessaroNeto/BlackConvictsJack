import pygame
from config import *

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Singleplayer", "Opções", "Sair"]
        self.selected_option = 0

        # Carregando imagens de personagem (5 placeholders)
        self.character_images = [pygame.Surface((100, 150)) for _ in range(5)]
        for i, surf in enumerate(self.character_images):
            surf.fill((100 + i*25, 30, 30))

    def draw_main_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Mesa dos Condenados", True, (255, 0, 0))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            label = self.font.render(option, True, color)
            self.screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, 250 + i * 50))

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option].lower()
        return None

    def draw_character_select(self):
        self.screen.fill((20, 20, 20))
        label = self.font.render("Escolha seu personagem", True, (255, 255, 255))
        self.screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 60))

        spacing = 40
        base_x = (SCREEN_WIDTH - (5 * 100 + 4 * spacing)) // 2
        for i, img in enumerate(self.character_images):
            self.screen.blit(pygame.transform.scale(img, (100, 150)), (base_x + i * (100 + spacing), 200))

    def handle_character_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            spacing = 40
            base_x = (SCREEN_WIDTH - (5 * 100 + 4 * spacing)) // 2
            for i in range(5):
                x = base_x + i * (100 + spacing)
                if x <= mx <= x + 100 and 200 <= my <= 350:
                    return i
        return None