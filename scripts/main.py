import pygame
from game import Game
from settings_page import SettingsPage

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    # Show settings page first
    settings_page = SettingsPage()
    settings = settings_page.show()

    # Start the game with the configured settings
    game = Game(settings)
    game.run()

    pygame.quit()
