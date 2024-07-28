import pygame
import random
from settings import default_settings

class Alien:
    def __init__(self):
        self.image = pygame.image.load('images/alien.png')  # Ensure you have an alien image file
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.reset()

    def reset(self):
        self.x = random.randint(0, default_settings['screen_width'] - self.width)
        self.y = random.randint(-100, -40)
        self.speed = random.uniform(0.5, 1.0)  # Adjusted speed for slower movement

    def update_position(self):
        self.y += self.speed
        if self.y > default_settings['screen_height']:
            self.reset()

    def has_reached_fighter(self, fighter):
        return self.y + self.height >= fighter.y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
