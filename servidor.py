import socket
import psutil

class Server:
    def __init__(self, host="0.0.0.0", port=5551):
        self.host = host
        self.port = port
        self.server_socket = None

    def format_memory(self, mem):
        """Formata as informações de memória RAM"""
        total = mem.total / (1024 ** 3)  # Convertendo para GB
        usada = mem.used / (1024 ** 3)
        livre = mem.available / (1024 ** 3)
        return f"Memória RAM Total: {total:.2f} GB\nMemória RAM Usada: {usada:.2f} GB\nMemória RAM Livre: {livre:.2f} GB"

    def format_disk(self):
        """Obtém e formata as informações do disco"""
        try:
            disk = psutil.disk_usage("C:\\")
            return f"Total: {disk.total / (1024 ** 3):.2f} GB, Usado: {disk.used / (1024 ** 3):.2f} GB, Livre: {disk.free / (1024 ** 3):.2f} GB, Uso: {disk.percent}%"
        except Exception as e:
            return f"Erro ao acessar o disco: {e}"

    def start_server(self):
        """Inicia o servidor e aguarda conexões"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor iniciado na porta {self.port}...")

        while True:
            try:
                clientsocket, address = self.server_socket.accept()
                print(f"Conexão de {address} estabelecida.")
                
                msg = clientsocket.recv(1024).decode("utf-8").strip()
                print(f"Comando recebido: {msg}")

                if msg == "/help":
                    resposta = (
                        "Comandos disponíveis:\n"
                        "/ram - Mostra a quantidade total, usada e livre de memória RAM\n"
                        "/hd - Mostra o espaço do disco\n"
                        "/cpu - Mostra a quantidade de processadores\n"
                        "/off - Desliga o servidor"
                    )

                elif msg == "/ram":
                    resposta = self.format_memory(psutil.virtual_memory())

                elif msg == "/hd":
                    resposta = self.format_disk()

                elif msg == "/cpu":
                    resposta = f"Cores físicos: {psutil.cpu_count(logical=False)}, Cores lógicos: {psutil.cpu_count(logical=True)}"

                elif msg == "/off":
                    resposta = "Desligando o servidor..."
                    clientsocket.send(resposta.encode("utf-8"))
                    clientsocket.close()
                    break  # Sai do loop e encerra o servidor

                else:
                    resposta = "Comando inválido. Use /help para ver os comandos disponíveis."

                clientsocket.send(resposta.encode("utf-8"))
                clientsocket.close()

            except Exception as e:
                print(f"Erro no servidor: {e}")

        self.server_socket.close()
        print("Servidor desligado.")


# Inicia o servidor
server = Server()
server.start_server()
