import pygame
import sys
import socket
import threading
import json
from fighter import Fighter
from alien import Alien
from ball import Ball
from game_music import GameMusic, SoundEffects
from generate_midi import generate_sound_files

# Constants for server connection
SERVER_IP = socket.gethostbyname(socket.gethostname())  # Update with your server IP address
SERVER_PORT = 12345

class Connection:
    def __init__(self):
        self.encoder = 'utf-8'
        self.header_length = 10
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            print("Connection established")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_data(self, data):
        try:
            data_json = json.dumps(data)
            header = str(len(data_json)).ljust(self.header_length)
            self.client_socket.send(header.encode(self.encoder))
            self.client_socket.send(data_json.encode(self.encoder))
        except Exception as e:
            print(f"Error sending data: {e}")

    def receive_data(self):
        try:
            header = self.client_socket.recv(self.header_length).decode(self.encoder).strip()
            if not header:
                return None
            packet_size = int(header)
            data = b""
            while len(data) < packet_size:
                packet = self.client_socket.recv(packet_size - len(data))
                if not packet:
                    return None
                data += packet
            return data.decode(self.encoder)
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

class Game:
    def __init__(self, settings, username):
        pygame.init()
        pygame.font.init()  # Ensure font module is initialized
        self.settings = settings
        self.username = username
        pygame.display.set_caption(self.settings['game_caption'])
        self.screen_width, self.screen_height = self.settings['screen_width'], self.settings['screen_height']
        self.screen_fill_color = self.settings['screen_fill_color']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_font = pygame.font.Font(None, 30)
        self.game_score = 0

        self.fighter = Fighter()
        self.alien = Alien()
        self.ball = Ball(self.fighter)

        self.clock = pygame.time.Clock()
        self.game_is_running = True

        self.connection = Connection()
        self.players = {}
        self.messages = []

        # Ensure sound files are created
        generate_sound_files()

        # Initialize game music with the provided background music file
        try:
            self.music = GameMusic('music/children_music_pretty.mid')
            self.music.play_background_music()
        except Exception as e:
            print(f"Error loading or playing music: {e}")

        # Initialize sound effects
        try:
            self.sound_effects = SoundEffects('effects/shoot_sound.mid', 'effects/collision_sound.mid')
        except Exception as e:
            print(f"Error loading sound effects: {e}")

        self.send_initial_data()

    def send_initial_data(self):
        initial_data = {'username': self.username}
        self.connection.send_data(initial_data)

    def run(self):
        threading.Thread(target=self.receive_game_state, daemon=True).start()  # Use daemon=True to allow threads to exit

        while self.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                    self.connection.client_socket.close()
                    pygame.quit()
                    sys.exit()
                self.handle_key_events(event)

            self.update_game_state()
            self.draw_screen()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        self.show_game_over()
        self.music.stop_background_music()  # Stop music when the game is over

    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.fighter.move_left()
            if event.key == pygame.K_RIGHT:
                self.fighter.move_right()
            if event.key == pygame.K_SPACE:
                self.ball.fire()
                self.sound_effects.play_shoot_sound()  # Play shoot sound

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.fighter.stop_moving()

    def update_game_state(self):
        self.fighter.update_position()
        self.alien.update_position()
        self.ball.update_position()

        if self.ball.is_out_of_screen():
            self.ball.reset()

        if self.ball.is_collision(self.alien):
            self.ball.reset()
            self.alien.reset()
            self.game_score += 1
            self.sound_effects.play_collision_sound()  # Play collision sound

        if self.alien.has_reached_fighter(self.fighter):
            self.game_is_running = False

        self.send_player_info()

    def send_player_info(self):
        player_info = {
            'username': self.username,
            'fighter_x': self.fighter.x,
            'fighter_y': self.fighter.y,
            'ball_x': self.ball.x,
            'ball_y': self.ball.y,
            'ball_fired': self.ball.was_fired
        }
        self.connection.send_data(player_info)

    def receive_game_state(self):
        while self.game_is_running:
            game_state_json = self.connection.receive_data()
            if game_state_json:
                try:
                    game_state = json.loads(game_state_json)
                    if isinstance(game_state, dict):
                        self.players = game_state
                    else:
                        self.messages.append(game_state)
                except json.JSONDecodeError:
                    print("Error decoding JSON:", game_state_json)
                    self.messages.append(game_state_json)

    def draw_screen(self):
        self.screen.fill(self.screen_fill_color)
        self.screen.blit(self.fighter.image, (self.fighter.x, self.fighter.y))
        self.draw_username(self.username, self.fighter.x, self.fighter.y)

        self.screen.blit(self.alien.image, (self.alien.x, self.alien.y))
        if self.ball.was_fired:
            self.screen.blit(self.ball.image, (self.ball.x, self.ball.y))

        for player in self.players.values():
            if player['username'] != self.username:
                # Render other players' fighters and balls here
                other_fighter = Fighter()
                other_fighter.x = player['fighter_x']
                other_fighter.y = player['fighter_y']
                self.screen.blit(other_fighter.image, (other_fighter.x, other_fighter.y))
                self.draw_username(player['username'], other_fighter.x, other_fighter.y)

                if player['ball_fired']:
                    other_ball = Ball(other_fighter)
                    other_ball.x = player['ball_x']
                    other_ball.y = player['ball_y']
                    self.screen.blit(other_ball.image, (other_ball.x, other_ball.y))

        self.show_game_score()
        self.show_info_box()
        self.show_messages()
        pygame.display.update()

    def draw_username(self, username, x, y):
        username_text = self.game_font.render(username, True, 'white')
        username_rect = username_text.get_rect(center=(x + 25, y - 20))  # Center above the fighter
        self.screen.blit(username_text, username_rect)

    def show_game_score(self):
        game_score_text = self.game_font.render(f"Your Score is: {self.game_score}", True, 'white')
        self.screen.blit(game_score_text, (20, 20))

    def show_info_box(self):
        info_box_text = self.game_font.render(f"Fighter Position: ({self.fighter.x}, {self.fighter.y})", True, 'white')
        self.screen.blit(info_box_text, (20, 50))

    def show_messages(self):
        for i, message in enumerate(self.messages[-5:], start=1):
            message_text = self.game_font.render(message, True, 'yellow')
            self.screen.blit(message_text, (20, self.screen_height - 20 * i))

    def show_game_over(self):
        game_over_text = self.game_font.render("Game Over", True, 'white')
        game_over_rectangle = game_over_text.get_rect()
        game_over_rectangle.center = (self.screen_width / 2, self.screen_height / 2)
        self.screen.blit(game_over_text, game_over_rectangle)
        pygame.display.update()
        pygame.time.wait(5000)
