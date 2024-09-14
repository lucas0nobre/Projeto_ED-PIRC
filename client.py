import socket

def iniciar_cliente():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
            # Conecta ao servidor na porta 65432 (mesmo endereço e porta do servidor)
            cliente_socket.connect(('localhost', 65432))
            
            print("Cliente conectado ao servidor.")
            print("Comandos disponíveis: criar <nome> <descrição>, ler [id], atualizar <id> <nome> <descrição>, deletar <id>")
            print("Digite 'sair' para encerrar o cliente.")
            
            while True:
                # Solicita ao usuário que insira o comando
                comando = input("\nDigite o comando: ").strip()
                
                if comando.lower() == 'sair':
                    print("Encerrando a conexão...")
                    break
                
                # Verifica se o comando não está vazio
                if not comando:
                    print("Comando vazio! Tente novamente.")
                    continue
                
                # Envia o comando para o servidor
                # Ajusta o comando para substituir espaços por "|" no caso de criar, atualizar
                try:
                    partes_comando = comando.split()
                    if partes_comando[0].lower() == "criar" and len(partes_comando) >= 3:
                        comando = f"criar|{partes_comando[1]}|{' '.join(partes_comando[2:])}"
                    elif partes_comando[0].lower() == "atualizar" and len(partes_comando) >= 4:
                        comando = f"atualizar|{partes_comando[1]}|{partes_comando[2]}|{' '.join(partes_comando[3:])}"
                    elif partes_comando[0].lower() == "deletar" and len(partes_comando) == 2:
                        comando = f"deletar|{partes_comando[1]}"
                    elif partes_comando[0].lower() == "ler":
                        if len(partes_comando) == 2:
                            comando = f"ler|{partes_comando[1]}"
                        else:
                            comando = "ler"
                    else:
                        print("Comando inválido. Tente novamente.")
                        continue

                    cliente_socket.sendall(comando.encode())
                except BrokenPipeError:
                    print("Erro: Conexão com o servidor foi perdida.")
                    break
                
                # Recebe a resposta do servidor
                try:
                    resposta = cliente_socket.recv(1024).decode()
                except ConnectionResetError:
                    print("Erro: Conexão com o servidor foi encerrada.")
                    break

                # Exibe a resposta do servidor
                print(f"Resposta do servidor: {resposta}")
    
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está em execução.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    iniciar_cliente()
