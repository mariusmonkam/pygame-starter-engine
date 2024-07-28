import pygame
import qrcode
import socket
import pyperclip
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

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def display_qr_code_and_link(img, link):
    img.save("qr_code.png")
    qr_image = pygame.image.load("qr_code.png")
    screen = pygame.display.set_mode((qr_image.get_width(), qr_image.get_height() + 100))
    pygame.display.set_caption("Connect to Game")

    font = pygame.font.Font(None, 30)
    link_text = font.render(link, True, (0, 0, 0))
    copy_button = pygame.Rect(10, qr_image.get_height() + 50, 200, 40)
    copy_text = font.render("Copy Link", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if copy_button.collidepoint(event.pos):
                    pyperclip.copy(link)
                    print("Link copied to clipboard!")

        screen.fill((255, 255, 255))
        screen.blit(qr_image, (0, 0))
        screen.blit(link_text, (10, qr_image.get_height() + 10))
        pygame.draw.rect(screen, (0, 0, 0), copy_button)
        screen.blit(copy_text, (20, qr_image.get_height() + 60))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    local_ip = get_local_ip()
    connection_data = f"http://{local_ip}:{SERVER_PORT}"
    qr_img = generate_qr_code(connection_data)
    display_qr_code_and_link(qr_img, connection_data)

    # Show settings page first
    settings_page = SettingsPage()
    settings = settings_page.show()

    # Prompt for username
    username = input("Enter your username: ")

    # Start the game with the configured settings
    game = Game(settings, username)
    game.run()

    pygame.quit()
