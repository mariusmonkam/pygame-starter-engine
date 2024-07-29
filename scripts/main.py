import os
import pygame
import socket
import http.server
import socketserver
from threading import Thread
from game import Game
from settings_page import SettingsPage

# Constants for server connection
SERVER_PORT = int(os.getenv('PORT', 12345))

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

def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", SERVER_PORT), handler)
    print(f"Serving on port {SERVER_PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    pygame.init()

    # Check if running on Heroku
    if 'DYNO' not in os.environ:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.font.init()  # Ensure font module is initialized

    local_ip = get_local_ip()
    connection_data = f"http://{local_ip}:{SERVER_PORT}"

    # Start the server in a separate thread
    server_thread = Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Show settings page with option to display QR code
    settings_page = SettingsPage()
    settings, username = settings_page.show()

    if settings is not None and username:
        # Start the game with the configured settings
        game = Game(settings, username)
        game.run()

    pygame.quit()
