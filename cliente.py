import socket
import psutil

class Cliente:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    def coletar_dados(self):
        """Coleta os dados do sistema."""
        memoria = psutil.virtual_memory()
        disco = psutil.disk_usage("C:\\")

        return {
            "host": socket.gethostname(),
            "cpu": psutil.cpu_count(logical=False),  # Cores físicos
            "ram": memoria.available // (1024 ** 2),  # Memória livre em MB
            "disco": disco.free // (1024 ** 3)  # Espaço livre em GB
        }

    def enviar_dados(self):
        """Envia os dados coletados para o servidor."""
        dados = self.coletar_dados()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
            cliente_socket.connect((self.server_host, self.server_port))
            cliente_socket.send(str(dados).encode())  # Envia os dados como string
            resposta = cliente_socket.recv(1024)
            print(resposta.decode())


# Inicia o cliente
cliente = Cliente('127.0.0.1', 5551)
cliente.enviar_dados()