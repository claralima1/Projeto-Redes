import socket
import threading

class Servidor:
    def __init__(self, host="0.0.0.0", port=5551):
        self.host = host
        self.port = port
        self.servidor_socket = None
        self.computadores_conectados = {}  # Armazena os dados dos clientes
        self.executando = True  # Controla se o servidor está em execução

    def calcular_media(self):
        """Calcula a média dos dados coletados."""
        if not self.computadores_conectados:
            return "Nenhum computador conectado."

        total_cpu = sum(info['cpu'] for info in self.computadores_conectados.values())
        total_ram = sum(info['ram'] for info in self.computadores_conectados.values())
        total_disco = sum(info['disco'] for info in self.computadores_conectados.values())
        count = len(self.computadores_conectados)

        return {
            "media_cpu": total_cpu / count,
            "media_ram": total_ram / count,
            "media_disco": total_disco / count
        }

    def listar_computadores(self):
        """Lista todos os computadores conectados."""
        if not self.computadores_conectados:
            return "Nenhum computador conectado."

        lista = "Computadores conectados:\n"
        for ip, info in self.computadores_conectados.items():
            lista += f"- {ip} (Host: {info['host']})\n"
        return lista

    def detalhar_computador(self, ip):
        """Mostra detalhes de um computador específico."""
        if ip not in self.computadores_conectados:
            return f"Computador com IP {ip} não encontrado."

        info = self.computadores_conectados[ip]
        detalhes = (
            f"Detalhes do computador {ip}:\n"
            f"Host: {info['host']}\n"
            f"CPU: {info['cpu']} cores\n"
            f"RAM Livre: {info['ram']} MB\n"
            f"Disco Livre: {info['disco']} GB"
        )
        return detalhes

    def handle_cliente(self, cliente_socket, endereco):
        """Lida com a conexão de um cliente."""
        try:
            print(f"Conexão de {endereco} estabelecida.")

            # Recebe os dados do cliente
            dados = cliente_socket.recv(1024).decode()
            dados = eval(dados)  # Converte a string para dicionário

            # Armazena os dados no dicionário
            ip = endereco[0]
            self.computadores_conectados[ip] = dados

            # Envia uma resposta
            cliente_socket.send(b"Dados recebidos com sucesso!")

        except Exception as e:
            print(f"Erro ao lidar com o cliente {endereco}: {e}")
        finally:
            cliente_socket.close()

    def iniciar_servidor(self):
        """Inicia o servidor e aguarda conexões."""
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.bind((self.host, self.port))
        self.servidor_socket.listen(5)
        print(f"Servidor iniciado na porta {self.port}...")

        # Inicia uma thread para o menu interativo
        threading.Thread(target=self.menu_interativo, daemon=True).start()

        while self.executando:
            try:
                cliente_socket, endereco = self.servidor_socket.accept()
                threading.Thread(target=self.handle_cliente, args=(cliente_socket, endereco)).start()
            except OSError:
                # Captura o erro quando o socket é fechado
                break

        print("Servidor parado.")

    def parar_servidor(self):
        """Para o servidor de forma segura."""
        print("Parando o servidor...")
        self.executando = False  # Encerra o loop principal
        self.servidor_socket.close()  # Fecha o socket do servidor

    def menu_interativo(self):
        """Menu interativo para visualizar os dados."""
        while self.executando:
            print("\n--- Menu do Servidor ---")
            print("1. Listar computadores conectados")
            print("2. Detalhar um computador")
            print("3. Calcular média dos dados")
            print("4. Parar servidor")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                print(self.listar_computadores())
            elif opcao == "2":
                print(self.listar_computadores())
                ip = input("Digite o IP do computador: ")
                print(self.detalhar_computador(ip))
            elif opcao == "3":
                media = self.calcular_media()
                print(f"Média dos dados:\nCPU: {media['media_cpu']} cores\nRAM: {media['media_ram']} MB\nDisco: {media['media_disco']} GB")
            elif opcao == "4":
                self.parar_servidor()
                break
            else:
                print("Opção inválida. Tente novamente.")


# Inicia o servidor
servidor = Servidor()
servidor.iniciar_servidor()