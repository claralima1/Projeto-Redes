import socket #comunicação de rede via socket
import psutil #módulo usado para acessar informações do sistema: CPU, memória, disco etc

class Cliente:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

    #Coleta os dados do sistema:
    def coletar_dados(self):
        memoria = psutil.virtual_memory() # O módulo chama o método que retorna a quantidade de memória RAM disponível
        disco = psutil.disk_usage("C:\\") # O módulo chama o método que retorna informações sobre o uso do disco 

        return {
            "host": socket.gethostname(), # Retorna o o endereço da máquina onde o código está sendo executado
            "cpu": psutil.cpu_count(logical=False),  # O módulo chama o método querRetorna o número de núcleos físicos da CPU
            "ram": memoria.available // (1024 ** 2),  # converte a Memória livre em MB
            "disco": disco.free // (1024 ** 3)  #Converte Espaço livre no disco em GB
        }
    
    #Envia os dados coletados para o servidor:
    def enviar_dados(self):
        dados = self.coletar_dados()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket: #Cria um socket TCP/IP (SOCK_STREAM) usando o protocolo IPv4 (AF_INET)
            cliente_socket.connect((self.server_host, self.server_port)) # Conecta o socket ao servidor no endereço e porta especificados
            cliente_socket.send(str(dados).encode())  # Converte o dicionário de dados em uma string, codifica-a em bytes e envia para o servidor
            resposta = cliente_socket.recv(1024) # Recebe uma resposta do servidor (até 1024 bytes)
            print(resposta.decode()) # Decodifica a resposta de bytes para string e a imprime


# Inicia o cliente
cliente = Cliente('127.0.0.1', 5551)
cliente.enviar_dados() # Enviar os dados do sistema para o servidor