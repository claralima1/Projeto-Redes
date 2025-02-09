
import socket 
import psutil
import json

class Cliente:
    def __init__(self, ip_servidor, porta_servidor):
        self.ip_servidor = ip_servidor
        self.porta_servidor = porta_servidor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def coletar_informacoes_sistema(self):

        dados = {
            "quantidade_cpu": psutil.cpu_count(logical=True),
            "ram_livre": psutil.virtual_memory().available,
            "disco_livre": psutil.disk_usage('/').free,
            "temperatura": self.coletar_temperatura_cpu()
        }
        return dados

    def coletar_temperatura_cpu(self):
        try:
            sensores = psutil.sensors_temperatures()
            if 'coretemp' in sensores:
                return sensores['coretemp'][0].current  
        except Exception:
            return None
        return None

    def enviar_dados(self, dados):
        mensagem = json.dumps(dados).encode()
        self.socket.sendall(mensagem)

    def receber_resposta(self):
        resposta = self.socket.recv(1024).decode()
        return resposta

    def conectar(self):
        self.socket.connect((self.ip_servidor, self.porta_servidor))

    def fechar_conexao(self):
        self.socket.close()

if __name__ == "__main__":
    cliente = Cliente('127.0.0.1', 65432)
    cliente.conectar()

    # Coleta as informações
    informacoes_sistema = cliente.coletar_informacoes_sistema()

    # Envia os dados para o servidor
    cliente.enviar_dados(informacoes_sistema)

    # Recebe resposta do servidor
    resposta = cliente.receber_resposta()
    print(f"Resposta do servidor: {resposta}")

    cliente.fechar_conexao()