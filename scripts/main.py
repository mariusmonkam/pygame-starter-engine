import pygame
import socket
from game import Game
from settings_page import SettingsPage

# Constants for server connection
SERVER_PORT = 12345

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.font.init()  # Ensure font module is initialized

    local_ip = get_local_ip()
    connection_data = f"http://{local_ip}:{SERVER_PORT}"
    
    # Show settings page with option to display QR code
    settings_page = SettingsPage()
    settings, username = settings_page.show()

    if settings is not None and username:
        # Start the game with the configured settings
        game = Game(settings, username)
        game.run()

    pygame.quit()
