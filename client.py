import socket

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Conecta ao servidor na porta 65432 (mesmo endereço e porta do servidor)
        client_socket.connect(('localhost', 65432))
        
        print("Cliente conectado ao servidor.")
        print("Comandos disponíveis: CREATE, READ, UPDATE, DELETE")
        
        while True:
            # Solicita ao usuário que insira o comando
            command = input("Digite o comando: ").strip()
            
            if command.lower() == 'exit':
                print("Encerrando a conexão...")
                break
            
            # Envia o comando para o servidor
            client_socket.sendall(command.encode())
            
            # Recebe a resposta do servidor
            response = client_socket.recv(1024).decode()
            
            # Exibe a resposta do servidor
            print(f"Resposta do servidor: {response}")

if __name__ == "__main__":
    start_client()  