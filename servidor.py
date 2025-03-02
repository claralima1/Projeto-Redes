import socket
import psutil

class Servidor:
    def __init__(self, host="0.0.0.0", port=5551):
        self.host = host
        self.port = port
        self.servidor_socket = None

    def formatar_memoria(self, memoria):
        """Formata as informações de memória RAM"""
        total = memoria.total / (1024 ** 3)  # Convertendo para GB
        usada = memoria.used / (1024 ** 3)
        livre = memoria.available / (1024 ** 3)
        return f"Memória RAM Total: {total:.2f} GB\nMemória RAM Usada: {usada:.2f} GB\nMemória RAM Livre: {livre:.2f} GB"

    def formatar_disco(self):
        """Obtém e formata as informações do disco"""
        try:
            disco = psutil.disk_usage("C:\\")
            return f"Total: {disco.total / (1024 ** 3):.2f} GB, Usado: {disco.used / (1024 ** 3):.2f} GB, Livre: {disco.free / (1024 ** 3):.2f} GB, Uso: {disco.percent}%"
        except Exception as e:
            return f"Erro ao acessar o disco: {e}"

    def iniciar_servidor(self):
        """Inicia o servidor e aguarda conexões"""
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.port))
        self.servidor_socket.listen(5)
        print(f"Servidor iniciado na porta {self.port}...")

        while True:
            try:
                cliente_socket, endereco = self.servidor_socket.accept()
                print(f"Conexão de {endereco} estabelecida.")
                
                mensagem = cliente_socket.recv(1024).decode("utf-8").strip()
                print(f"Comando recebido: {mensagem}")

                if mensagem == "/help":
                    resposta = (
                        "Comandos disponíveis:\n"
                        "/ram - Mostra a quantidade total, usada e livre de memória RAM\n"
                        "/hd - Mostra o espaço do disco\n"
                        "/cpu - Mostra a quantidade de processadores\n"
                        "/off - Desliga o servidor"
                    )

                elif mensagem == "/ram":
                    resposta = self.formatar_memoria(psutil.virtual_memory())

                elif mensagem == "/hd":
                    resposta = self.formatar_disco()

                elif mensagem == "/cpu":
                    resposta = f"Cores físicos: {psutil.cpu_count(logical=False)}, Cores lógicos: {psutil.cpu_count(logical=True)}"

                elif mensagem == "/off":
                    resposta = "Desligando o servidor..."
                    cliente_socket.send(resposta.encode("utf-8"))
                    cliente_socket.close()
                    break  # Sai do loop e encerra o servidor

                else:
                    resposta = "Comando inválido. Use /help para ver os comandos disponíveis."

                cliente_socket.send(resposta.encode("utf-8"))
                cliente_socket.close()

            except Exception as e:
                print(f"Erro no servidor: {e}")

        self.servidor_socket.close()
        print("Servidor desligado.")


# Inicia o servidor
servidor = Servidor()
servidor.iniciar_servidor()
