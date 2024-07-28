import pygame
import sys
from settings import default_settings

class SettingsPage:
    def __init__(self):
        self.screen = pygame.display.set_mode((default_settings['screen_width'], default_settings['screen_height']))
        pygame.display.set_caption("Game Settings")
        self.font = pygame.font.Font(None, 30)
        self.settings = default_settings.copy()
        self.running = True

        # Button settings
        self.button_color = (0, 255, 0)
        self.button_hover_color = (0, 200, 0)
        self.button_rect = pygame.Rect(350, 500, 100, 50)  # Adjusted position and size
        self.button_text = self.font.render("Start", True, 'black')
        self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)

    def show(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.running = False

            self.screen.fill(self.settings['screen_fill_color'])
            self.display_settings()
            self.draw_button()
            pygame.display.update()
        
        return self.settings

    def display_settings(self):
        y = 50
        for key, value in self.settings.items():
            setting_text = self.font.render(f"{key}: {value}", True, 'white')
            self.screen.blit(setting_text, (50, y))
            y += 40

    def draw_button(self):
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color

        pygame.draw.rect(self.screen, button_color, self.button_rect)
        self.screen.blit(self.button_text, self.button_text_rect)
