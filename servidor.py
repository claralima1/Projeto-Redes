import socket
import json
import ssl
from statistics import mean

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def listen(self):
        """ Escuta por conexões """
        self.socket.listen(5)
        print(f"Servidor ouvindo na porta {self.port}...")
        
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Conexão recebida de {client_address}")
            
            # Criptografia SSL
            secure_client_socket = self.context.wrap_socket(client_socket, server_side=True)
            
            # Recebe os dados do cliente
            data = secure_client_socket.recv(1024)
            if data:
                self.process_data(data, secure_client_socket)
            secure_client_socket.close()

    def process_data(self, data, client_socket):
        """ Processa os dados recebidos do cliente """
        data = json.loads(data.decode())
        
        # Calculando a média dos valores recebidos
        cpu_count = data["cpu_count"]
        ram_free = data["ram_free"] / (1024 * 1024 * 1024)  # Convertendo de bytes para GB
        disk_free = data["disk_free"] / (1024 * 1024 * 1024)  # Convertendo de bytes para GB
        temperature = data["temperature"]

        average = mean([cpu_count, ram_free, disk_free, temperature if temperature else 0])

        # Enviando a resposta de volta ao cliente
        response = {
            "average": average,
            "details": {
                "cpu_count": cpu_count,
                "ram_free": ram_free,
                "disk_free": disk_free,
                "temperature": temperature
            }
        }
        client_socket.sendall(json.dumps(response).encode())

if __name__ == "__main__":
    server = Server('127.0.0.1', 65433)
    server.listen()
