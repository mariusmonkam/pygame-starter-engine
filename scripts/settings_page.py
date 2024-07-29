import pygame
import qrcode
import pyperclip
import time
import sys

class SettingsPage:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.background_color = (255, 255, 255)
        self.button_color = (0, 0, 0)
        self.button_text_color = (255, 255, 255)
        self.button_hover_color = (50, 50, 50)
        self.font = pygame.font.Font(None, 36)
        self.username = ""

    def show(self):
        pygame.init()
        pygame.font.init()  # Ensure font module is initialized
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Settings")

        start_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 - 25, 200, 50)
        invite_button = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)
        input_box = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 - 100, 200, 50)
        input_label = self.font.render("Username:", True, (0, 0, 0))

        running = True
        active_input = False
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive

        while running:
            screen.fill(self.background_color)
            mx, my = pygame.mouse.get_pos()

            # Draw buttons
            self.draw_button(screen, start_button, "Start", mx, my)
            self.draw_button(screen, invite_button, "Invite Player", mx, my)

            # Draw input box and label
            screen.blit(input_label, (input_box.x - 110, input_box.y + 10))
            txt_surface = self.font.render(self.username, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active_input = not active_input
                    else:
                        active_input = False
                    if start_button.collidepoint(event.pos):
                        pygame.quit()
                        return {
                            'game_caption': 'Game Title',
                            'screen_width': 800,
                            'screen_height': 600,
                            'screen_fill_color': (0, 0, 0)
                        }, self.username
                    if invite_button.collidepoint(event.pos):
                        self.display_qr_code_and_link("http://example.com")

                    color = color_active if active_input else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active_input:
                        if event.key == pygame.K_RETURN:
                            active_input = False
                            color = color_inactive
                        elif event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += event.unicode

            pygame.display.update()

    def draw_button(self, screen, button_rect, text, mx, my):
        if button_rect.collidepoint((mx, my)):
            color = self.button_hover_color
        else:
            color = self.button_color
        pygame.draw.rect(screen, color, button_rect)
        text_surface = self.font.render(text, True, self.button_text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    def generate_qr_code(self, data):
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

    def display_qr_code_and_link(self, link, display_duration=30):
        img = self.generate_qr_code(link)
        img.save("qr_code.png")
        qr_image = pygame.image.load("qr_code.png")
        screen = pygame.display.set_mode((qr_image.get_width(), qr_image.get_height() + 100))
        pygame.display.set_caption("Connect to Game")

        font = pygame.font.Font(None, 30)
        link_text = font.render(link, True, (0, 0, 0))
        copy_button = pygame.Rect(10, qr_image.get_height() + 50, 200, 40)
        close_button = pygame.Rect(qr_image.get_width() - 110, qr_image.get_height() + 50, 100, 40)
        copy_text = font.render("Copy Link", True, (255, 255, 255))
        close_text = font.render("Close", True, (255, 255, 255))

        start_time = time.time()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if copy_button.collidepoint(event.pos):
                        pyperclip.copy(link)
                        print("Link copied to clipboard!")
                    if close_button.collidepoint(event.pos):
                        running = False

            current_time = time.time()
            if current_time - start_time > display_duration:
                running = False

            screen.fill((255, 255, 255))
            screen.blit(qr_image, (0, 0))
            screen.blit(link_text, (10, qr_image.get_height() + 10))
            pygame.draw.rect(screen, (0, 0, 0), copy_button)
            screen.blit(copy_text, (20, qr_image.get_height() + 60))
            pygame.draw.rect(screen, (0, 0, 0), close_button)
            screen.blit(close_text, (qr_image.get_width() - 90, qr_image.get_height() + 60))
            pygame.display.update()

        # Return to settings screen after closing the QR code display
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Settings")
