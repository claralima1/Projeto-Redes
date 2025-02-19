import socket

class Cliente:
    def __init__(self, host="127.0.0.1", porta=5000):
        self.host = host
        self.porta = porta

    def conectar_servidor(self):
        """Conecta-se ao servidor e recebe o número de CPUs."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((self.host, self.porta))
            num_cpus = cliente.recv(1024).decode()
            print(f"Número de CPUs do servidor: {num_cpus}")


cliente = Cliente()
cliente.conectar_servidor()
