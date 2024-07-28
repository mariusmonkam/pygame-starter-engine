import pygame
from settings import default_settings

class Ball:
    def __init__(self, fighter):
        self.image = pygame.image.load('images/ball.png')  # Ensure you have a ball image file
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.fighter = fighter  # Store the fighter reference
        self.reset()

    def reset(self):
        self.x = self.fighter.x + self.fighter.width // 2 - self.width // 2
        self.y = self.fighter.y - self.height
        self.step = 5
        self.was_fired = False

    def update_position(self):
        if self.was_fired:
            self.y -= self.step

    def fire(self):
        if not self.was_fired:
            self.x = self.fighter.x + self.fighter.width // 2 - self.width // 2
            self.y = self.fighter.y - self.height
            self.was_fired = True

    def is_out_of_screen(self):
        return self.y < 0

    def is_collision(self, alien):
        return (
            self.x < alien.x + alien.width and
            self.x + self.width > alien.x and
            self.y < alien.y + alien.height and
            self.y + self.height > alien.y
        )

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
