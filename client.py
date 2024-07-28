import pygame
import socket
import threading
import json
import time

# Constants
DEST_IP = socket.gethostbyname(socket.gethostname())
DEST_PORT = 12345

class Connection:
    def __init__(self):
        self.encoder = "utf-8"
        self.header_length = 10
        self.player_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.player_socket.connect((DEST_IP, DEST_PORT))
            print("Connection established")
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def receive_data(self):
        try:
            header = self.player_socket.recv(self.header_length).decode(self.encoder).strip()
            if not header:
                print("No header received")
                return None
            packet_size = int(header)
            print(f"Packet size to receive: {packet_size}")
            data = b""
            while len(data) < packet_size:
                packet = self.player_socket.recv(packet_size - len(data))
                if not packet:
                    print("No data packet received")
                    return None
                data += packet
            return data.decode(self.encoder)
        except Exception as e:
            print(f"Error receiving data: {e}")
            return None

class Player:
    def __init__(self):
        self.init_empty()

    def init_empty(self):
        self.number = 0
        self.size = 0
        self.score = 0
        self.starting_x = 0
        self.starting_y = 0
        self.p_color = (0, 0, 0)
        self.s_color = (0, 0, 0)
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.coord = (0, 0, 0, 0)
        self.is_waiting = False
        self.is_ready = False
        self.is_playing = False
        self.status_message = ""

    def set_player_info(self, player_info):
        for key, value in player_info.items():
            setattr(self, key, value)
        self.p_color = tuple(self.p_color)
        self.s_color = tuple(self.s_color)
        self.coord = tuple(self.coord)

class Game:
    def __init__(self, connection):
        self.connection = connection
        self.player = Player()
        self.game_active = True
        self.players = []

        try:
            self.receive_initial_data()
            self.players = [None] * self.TOTAL_PLAYERS

            self.receive_player_data()

            self.ready_game()

            pygame.init()
            self.screen = pygame.display.set_mode((self.ROOM_SIZE, self.ROOM_SIZE))
            self.clock = pygame.time.Clock()
            pygame.display.set_caption("Client Window")
        except Exception as e:
            print(f"Error initializing game: {e}")
            self.game_active = False

    def receive_initial_data(self):
        try:
            initial_data_json = self.connection.receive_data()
            if initial_data_json:
                initial_data = json.loads(initial_data_json)
                self.ROOM_SIZE = initial_data['ROOM_SIZE']
                self.ROUND_TIME = initial_data['ROUND_TIME']
                self.FPS = initial_data['FPS']
                self.TOTAL_PLAYERS = initial_data['TOTAL_PLAYERS']
                print("Initial data received and set")
            else:
                print("No initial data received")
                raise ValueError("No initial data received")
        except Exception as e:
            print(f"Error receiving initial data: {e}")
            raise

    def receive_player_data(self):
        try:
            player_info_json = self.connection.receive_data()
            if player_info_json:
                player_info = json.loads(player_info_json)
                self.player.set_player_info(player_info)
                print("Player data received and initialized")
            else:
                print("No player data received")
                raise ValueError("No player data received")
        except Exception as e:
            print(f"Error receiving player data: {e}")
            raise

    def ready_game(self):
        self.player.is_waiting = False
        self.player.is_ready = True
        self.player.is_playing = False
        self.send_player_info()

    def send_player_info(self):
        try:
            player_info = {
                'coord': self.player.coord,
                'is_waiting': self.player.is_waiting,
                'is_ready': self.player.is_ready,
                'is_playing': self.player.is_playing,
            }
            player_info_json = json.dumps(player_info)
            header = str(len(player_info_json)).ljust(self.connection.header_length)
            self.connection.player_socket.send(header.encode(self.connection.encoder))
            self.connection.player_socket.send(player_info_json.encode(self.connection.encoder))
            print("Player info sent")
        except Exception as e:
            print(f"Error sending player info: {e}")

    def receive_game_state(self):
        while self.game_active:
            try:
                game_state_json = self.connection.receive_data()
                if game_state_json:
                    game_state = json.loads(game_state_json)
                    for i, player_json in enumerate(game_state):
                        if i < len(self.players):
                            player_info = json.loads(player_json)
                            if not self.players[i]:
                                self.players[i] = Player()
                            self.players[i].set_player_info(player_info)
                    self.ROUND_TIME = self.receive_int()
                    self.update_display()
                else:
                    print("No game state received")
                    time.sleep(1)
            except Exception as e:
                print(f"Error receiving game state: {e}")
                time.sleep(1)

    def receive_int(self):
        try:
            data = self.connection.receive_data()
            return int(data) if data else 0
        except Exception as e:
            print(f"Error receiving integer: {e}")
            return 0

    def update_display(self):
        try:
            self.screen.fill((0, 0, 0))
            for player in self.players:
                if player:
                    pygame.draw.rect(self.screen, player.p_color, player.coord)
                    pygame.draw.rect(self.screen, player.s_color, player.coord, 5)
            pygame.display.update()
            self.clock.tick(self.FPS)
        except Exception as e:
            print(f"Error updating display: {e}")

    def process_game_state(self):
        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_active = False
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.dx = -1
                self.player.dy = 0
            elif keys[pygame.K_RIGHT]:
                self.player.dx = 1
                self.player.dy = 0
            elif keys[pygame.K_UP]:
                self.player.dx = 0
                self.player.dy = -1
            elif keys[pygame.K_DOWN]:
                self.player.dx = 0
                self.player.dy = 1

            self.player.x += self.player.dx * self.player.size
            self.player.y += self.player.dy * self.player.size
            self.player.coord = (self.player.x, self.player.y, self.player.size, self.player.size)

            self.send_player_info()
            self.update_display()

    def run(self):
        threading.Thread(target=self.receive_game_state).start()
        self.process_game_state()

if __name__ == "__main__":
    try:
        my_connection = Connection()
        my_game = Game(my_connection)
        my_game.run()
    except Exception as e:
        print(f"Error running game: {e}")
