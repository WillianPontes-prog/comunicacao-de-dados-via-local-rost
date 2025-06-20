# network.py
import socket
import threading

class NetworkManager:
    def __init__(self, host, port, is_server=False, on_receive_callback=None):
        self.host = host
        self.port = port
        self.is_server = is_server
        self.on_receive_callback = on_receive_callback
        self.sock = None
        self.connection = None # Para o cliente, é o próprio socket; para o servidor, é o socket do cliente conectado

    def start(self):
        if self.is_server:
            self._start_server()
        else:
            self._start_client()

    def _start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Servidor escutando em {self.host}:{self.port}")
        self.server_thread = threading.Thread(target=self._accept_connections)
        self.server_thread.daemon = True
        self.server_thread.start()

    def _accept_connections(self):
        try:
            self.connection, addr = self.sock.accept()
            print(f"Conexão estabelecida com {addr}")
            self._start_receive_thread(self.connection)
        except Exception as e:
            print(f"Erro ao aceitar conexão: {e}")

    def _start_client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.host, self.port))
            self.connection = self.sock
            print(f"Conectado ao servidor em {self.host}:{self.port}")
            self._start_receive_thread(self.connection)
        except ConnectionRefusedError:
            print(f"Conexão recusada. Verifique se o servidor está ativo em {self.host}:{self.port}")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def _start_receive_thread(self, conn):
        self.receive_thread = threading.Thread(target=self._receive_data, args=(conn,))
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def _receive_data(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    print("Conexão fechada pelo peer.")
                    break
                if self.on_receive_callback:
                    self.on_receive_callback(data.decode('latin-1')) # Usar latin-1 para compatibilidade com ASCII estendido
            except ConnectionResetError:
                print("Conexão resetada pelo peer.")
                break
            except Exception as e:
                print(f"Erro ao receber dados: {e}")
                break

    def send_data(self, data):
        if self.connection:
            try:
                self.connection.sendall(data.encode('latin-1')) # Usar latin-1 para compatibilidade com ASCII estendido
            except Exception as e:
                print(f"Erro ao enviar dados: {e}")
        else:
            print("Nenhuma conexão ativa para enviar dados.")

    def close(self):
        if self.connection:
            self.connection.close()
        if self.sock:
            self.sock.close()
        print("Conexão de rede fechada.")

# Exemplo de uso (em scripts separados para teste):
# No lado do servidor (ex: server_test.py):
# from network import NetworkManager
# def handle_received_data(data):
#     print(f"Servidor recebeu: {data}")
# server = NetworkManager('0.0.0.0', 12345, is_server=True, on_receive_callback=handle_received_data)
# server.start()
# input("Pressione Enter para parar o servidor...") # Mantém o servidor rodando
# server.close()

# No lado do cliente (ex: client_test.py):
# from network import NetworkManager
# def handle_received_data(data):
#     print(f"Cliente recebeu: {data}")
# client = NetworkManager('127.0.0.1', 12345, is_server=False, on_receive_callback=handle_received_data)
# client.start()
# client.send_data("Olá do cliente!")
# input("Pressione Enter para parar o cliente...")
# client.close()