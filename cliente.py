import socket

class Cliente:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta

    def conectar_servidor(self):
        """Conecta-se ao servidor e recebe o número de CPUs."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((self.host, self.porta))
            num_cpus = cliente.recv(1024).decode()
            print(f"Número de CPUs do servidor: {num_cpus}")


cliente = Cliente("127.0.0.1", 5000)
cliente.conectar_servidor()
