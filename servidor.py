import socket # Módulo para gerenciar conexões de rede entre o servidor e os clientes
import threading # Módulo que Permite que o servidor lide com múltiplos clientes simultaneamente

class Servidor:
    def __init__(self, host="0.0.0.0", port=5551): # "0.0.0.0" significa que o servidor aceita conexões de qualquer interface de rede
        self.host = host
        self.port = port
        self.servidor_socket = None # Socket que o servidor usa para aceitar conexões
        self.computadores_conectados = {}  # Armazena em um dicionário os dados dos clientes (A chave é o IP do cliente)
        self.executando = True  # Controla se o servidor está em execução

    #####################################################################################
    #VERIFICAR COMO É PRA SER FEITA A MÉDIA DOS DADOS

    def calcular_media(self):
        if not self.computadores_conectados: # Verifica se há clientes conectados
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
    #####################################################################################

    def listar_computadores(self):
        if not self.computadores_conectados: # Verifica se há clientes conectados
            return "Nenhum computador conectado"

        lista = "Computadores conectados:\n" 
        for ip, info in self.computadores_conectados.items(): # Itera sobre o dicionário
            lista += f"- {ip} (Host: {info['host']})\n"  # 
        return lista

    def detalhar_computador(self, ip):
        if ip not in self.computadores_conectados:
            return f"Computador com IP {ip} não encontrado"

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

    #Inicia o servidor e aguarda conexões:
    def iniciar_servidor(self):
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

    #Para o servidor de forma segura:
    def parar_servidor(self):
        print("Parando o servidor...")
        self.executando = False  # Encerra o loop principal
        self.servidor_socket.close()  # Fecha o socket do servidor

    #Menu interativo para visualizar os dados:
    def menu_interativo(self):
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