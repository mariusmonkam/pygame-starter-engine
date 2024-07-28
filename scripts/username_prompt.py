import pygame
import sys

class UsernamePrompt:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Enter Username")
        self.font = pygame.font.Font(None, 30)
        self.username = ""
        self.running = True

    def show(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode

            self.screen.fill((0, 0, 0))
            prompt_text = self.font.render("Enter your username:", True, 'white')
            username_text = self.font.render(self.username, True, 'white')
            self.screen.blit(prompt_text, (20, 50))
            self.screen.blit(username_text, (20, 100))
            pygame.display.update()

        return self.username
