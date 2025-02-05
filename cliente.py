import socket
import psutil
import json
import ssl

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.socket = self.context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=server_ip)

    def get_system_info(self):
        """ Coleta informações do sistema """
        data = {
            "cpu_count": psutil.cpu_count(logical=True),
            "ram_free": psutil.virtual_memory().available,
            "disk_free": psutil.disk_usage('/').free,
            "temperature": self.get_cpu_temperature()
        }
        return data

    def get_cpu_temperature(self):
        """ Coleta a temperatura do processador """
        try:
            sensors = psutil.sensors_temperatures()
            if 'coretemp' in sensors:
                return sensors['coretemp'][0].current  # A temperatura do primeiro núcleo
        except Exception as e:
            return "Temperatura não disponível"
        return None

    def send_data(self, data):
        """ Envia os dados ao servidor """
        message = json.dumps(data).encode()
        self.socket.sendall(message)

    def receive_response(self):
        """ Recebe a resposta do servidor """
        response = self.socket.recv(1024).decode()
        return response

    def connect(self):
        """ Conecta ao servidor """
        self.socket.connect((self.server_ip, self.server_port))

    def close(self):
        """ Fecha a conexão com o servidor """
        self.socket.close()

if __name__ == "__main__":
    client = Client('127.0.0.1', 65432)
    client.connect()

    # Coleta as informações
    system_info = client.get_system_info()

    # Envia os dados para o servidor
    client.send_data(system_info)

    # Recebe resposta do servidor
    response = client.receive_response()
    print(f"Resposta do servidor: {response}")

    client.close()
