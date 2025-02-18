
import socket
import json
from statistics import mean #importa do módulo a função "mean" para calcular a media dos dados

class Servidor:
    def __init__(self, endereco, porta):
        self.endereco = endereco
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um socket (AF_INET = IPv4(protocolo utilizado)) (SOCK_STREAM = define o tipo de socket (TCP))
        self.socket.bind((self.endereco, self.porta)) #função para associar um socket a um endereço IP e porta que o servidor estará usando para ouvir conexões

    def escutar(self): #Função que faz o servidor começar a escutar conexões de clientes
        self.socket.listen(5) #5 é o número de conexões que o servidor pode ter na fila
        print(f"Servidor ouvindo na porta {self.porta}...")

        while True: #loop para esperar por novas conexões
            socket_cliente, endereco_cliente = self.socket.accept() #aguarda a conexão de um cliente | Quando um cliente se conecta, "accept()" retorna dois valores(socket_cliente e  endereco_cliente)
            print(f"Conexão recebida de {endereco_cliente}")

            # Recebe os dados do cliente
            dados = socket_cliente.recv(1024) #lê até 1024 bytes (amanho de buffer)
            if dados: #se o cliente enviar algo
                self.processar_dados(dados, socket_cliente) #processa as informações recebidas
            socket_cliente.close() #Depois de processar os dados, a conexão com o cliente é fechada (para liberar os recursos do sitema)

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
