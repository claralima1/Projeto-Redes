import socket
import os

class Servidor:
    def __init__(self, host="0.0.0.0", porta=5000):
        self.host = host
        self.porta = porta

    def obter_numero_cpus(self):
        return os.cpu_count()

    def iniciar(self):
        """Inicia o servidor e aguarda conexões."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind((self.host, self.porta))
            servidor.listen(5)
            print(f"Servidor aguardando conexões em {self.host}:{self.porta}...")

            while True:
                conexao, endereco = servidor.accept()
                print(f"Cliente conectado: {endereco}")

                num_cpus = self.obter_numero_cpus()
                conexao.sendall(str(num_cpus).encode())

                conexao.close()


servidor = Servidor()
servidor.iniciar()
