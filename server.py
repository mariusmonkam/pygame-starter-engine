import socket
import threading
import json
import time

# Define constants
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345

# Pygame constants
ROOM_SIZE = 700
PLAYER_SIZE = 140
ROUND_TIME = 30
FPS = 15
TOTAL_PLAYERS = 4

while ROOM_SIZE % PLAYER_SIZE != 0:
    PLAYER_SIZE += 1

if TOTAL_PLAYERS > 4:
    TOTAL_PLAYERS = 4

class Connection:
    def __init__(self):
        self.encoder = 'utf-8'
        self.header_length = 10
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST_IP, HOST_PORT))
        self.server_socket.listen()

class Player:
    def __init__(self, number):
        self.number = number
        self.size = PLAYER_SIZE
        self.score = 0
        self.starting_x = (number - 1) * PLAYER_SIZE
        self.starting_y = 0
        self.p_color = (255 // number, 0, 0)
        self.s_color = (150 // number, 0, 0)
        self.x = self.starting_x
        self.y = self.starting_y
        self.dx = 0
        self.dy = 0
        self.coord = (self.x, self.y, self.size, self.size)
        self.is_waiting = True
        self.is_ready = False
        self.is_playing = False
        self.status_message = f"Waiting for {TOTAL_PLAYERS} total players"

    def set_player_info(self, player_info):
        self.coord = tuple(player_info['coord'])
        self.is_waiting = player_info['is_waiting']
        self.is_ready = player_info['is_ready']
        self.is_playing = player_info['is_playing']

class GameServer:
    def __init__(self):
        self.connection = Connection()
        self.players = []
        self.client_handlers = []
        self.game_active = False

    def start_server(self):
        print(f"Server is listening on {HOST_IP}:{HOST_PORT}")
        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.connection.server_socket.accept()
            if len(self.players) < TOTAL_PLAYERS:
                player_number = len(self.players) + 1
                player = Player(player_number)
                self.players.append(player)
                print(f"New player joining from {client_address}...Total players: {len(self.players)}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, player))
                client_handler.start()
                self.client_handlers.append(client_handler)

                if len(self.players) == TOTAL_PLAYERS:
                    self.start_game()
            else:
                print(f"New player attempted to join from {client_address} but room is full")

    def handle_client(self, client_socket, player):
        try:
            initial_data = {
                'ROOM_SIZE': ROOM_SIZE,
                'ROUND_TIME': ROUND_TIME,
                'FPS': FPS,
                'TOTAL_PLAYERS': TOTAL_PLAYERS
            }
            initial_data_json = json.dumps(initial_data)
            header = str(len(initial_data_json)).ljust(self.connection.header_length)
            client_socket.send(header.encode(self.connection.encoder))
            client_socket.send(initial_data_json.encode(self.connection.encoder))
            print("Initial data sent to player")

            player_data_json = json.dumps(player.__dict__)
            header = str(len(player_data_json)).ljust(self.connection.header_length)
            client_socket.send(header.encode(self.connection.encoder))
            client_socket.send(player_data_json.encode(self.connection.encoder))
            print(f"Player info sent to player {player.number}")

            while self.game_active:
                try:
                    header = client_socket.recv(self.connection.header_length).decode(self.connection.encoder).strip()
                    if not header:
                        break
                    packet_size = int(header)
                    data = b""
                    while len(data) < packet_size:
                        packet = client_socket.recv(packet_size - len(data))
                        if not packet:
                            break
                        data += packet
                    player_info = json.loads(data.decode(self.connection.encoder))
                    player.set_player_info(player_info)
                    self.broadcast_game_state()
                except Exception as e:
                    print(f"Error receiving pregame player info: {e}")
                    break
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def start_game(self):
        self.game_active = True
        for player in self.players:
            player.is_waiting = False
            player.is_ready = True
            player.is_playing = True
        self.broadcast_game_state()
        print("Game started")

    def broadcast_game_state(self):
        game_state = [json.dumps(player.__dict__) for player in self.players]
        game_state_json = json.dumps(game_state)
        header = str(len(game_state_json)).ljust(self.connection.header_length)
        for player in self.players:
            try:
                player.client_socket.send(header.encode(self.connection.encoder))
                player.client_socket.send(game_state_json.encode(self.connection.encoder))
                print("Broadcast game state to all players")
            except Exception as e:
                print(f"Error broadcasting game state: {e}")

if __name__ == "__main__":
    game_server = GameServer()
    game_server.start_server()
