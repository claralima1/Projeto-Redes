
import socket
import json
from statistics import mean

class Servidor:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.endereco, self.porta))

    def escutar(self):
        self.socket.listen(5)
        print(f"Servidor ouvindo na porta {self.porta}...")

        while True:
            socket_cliente, endereco_cliente = self.socket.accept()
            print(f"Conexão recebida de {endereco_cliente}")

            # Recebe os dados do cliente
            dados = socket_cliente.recv(1024)
            if dados:
                self.processar_dados(dados, socket_cliente)
            socket_cliente.close()

    def processar_dados(self, dados, socket_cliente):
        """ Processa os dados recebidos do cliente """
        dados = json.loads(dados.decode())

        # Calculando a média dos valores recebidos
        quantidade_cpu = dados["quantidade_cpu"]
        ram_livre = dados["ram_livre"] / (1024 * 1024 * 1024)  # Convertendo de bytes para GB
        disco_livre = dados["disco_livre"] / (1024 * 1024 * 1024)  # Convertendo de bytes para GB
        temperatura = dados["temperatura"] if dados["temperatura"] is not None else 0

        media = mean([quantidade_cpu, ram_livre, disco_livre, temperatura])


        resposta = {
            "media": media,
            "detalhes": {
                "quantidade_cpu": quantidade_cpu,
                "ram_livre": ram_livre,
                "disco_livre": disco_livre,
                "temperatura": temperatura
            }
        }
        socket_cliente.sendall(json.dumps(resposta).encode())

if __name__ == "__main__":
    servidor = Servidor('127.0.0.1', 65432)
    servidor.escutar()
