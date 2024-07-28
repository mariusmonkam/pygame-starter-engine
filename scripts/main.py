import pygame
from game import Game

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

game = Game()
game.run()

pygame.quit()
