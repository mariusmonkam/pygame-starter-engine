import socket
import threading
import json

class Server:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        print(f"Server is listening on {self.server_ip}:{self.server_port}")

        self.clients = []
        self.client_threads = []
        self.players = {}

    def broadcast(self, data):
        for client in self.clients:
            try:
                header = str(len(data)).ljust(10)
                client.send(header.encode('utf-8') + data.encode('utf-8'))
            except Exception as e:
                print(f"Error sending data: {e}")

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")
        self.clients.append(client_socket)
        try:
            while True:
                header = client_socket.recv(10).decode('utf-8').strip()
                if not header:
                    break
                packet_size = int(header)
                data = client_socket.recv(packet_size).decode('utf-8')
                player_data = json.loads(data)
                self.players[player_data['username']] = player_data
                self.broadcast(json.dumps(self.players))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(f"Connection closed from {address}")
            self.clients.remove(client_socket)
            if player_data['username'] in self.players:
                del self.players[player_data['username']]
            self.broadcast(json.dumps(self.players))
            client_socket.close()

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
            self.client_threads.append(client_thread)

if __name__ == "__main__":
    local_ip = socket.gethostbyname(socket.gethostname())
    server = Server(local_ip, 12345)
    server.start()
