import socket  # Biblioteca para comunicação em rede

# Função para estabelecer a conexão com o servidor
def conectar_ao_servidor():
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria o socket do cliente
        cliente_socket.connect(('localhost', 65432))  # Conecta ao servidor no localhost e porta 65432
        print("Cliente conectado ao servidor.")  # Confirma a conexão
        return cliente_socket  # Retorna o socket do cliente
    except ConnectionRefusedError:  # Trata o erro se a conexão for recusada (servidor não está em execução)
        print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está em execução.")
        return None
    except Exception as e:  # Captura outros erros imprevistos
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# Função para enviar comandos ao servidor
def enviar_comando(cliente_socket, comando):
    try:
        cliente_socket.sendall(comando.encode())  # Envia o comando codificado para o servidor
    except BrokenPipeError:  # Captura o erro se a conexão com o servidor for interrompida
        print("Erro: Conexão com o servidor foi perdida.")
        return False  # Retorna False indicando falha ao enviar o comando
    except Exception as e:  # Captura outros erros imprevistos ao enviar o comando
        print(f"Erro ao enviar comando: {e}")
        return False
    return True  # Retorna True se o envio foi bem-sucedido

# Função para receber a resposta do servidor
def receber_resposta(cliente_socket):
    try:
        resposta = cliente_socket.recv(1024).decode()  # Recebe a resposta do servidor (até 1024 bytes)
        return resposta  # Retorna a resposta decodificada
    except ConnectionResetError:  # Captura o erro se a conexão for encerrada pelo servidor
        print("Erro: Conexão com o servidor foi encerrada.")
    except Exception as e:  # Captura outros erros ao tentar receber a resposta
        print(f"Erro ao receber resposta: {e}")
    return None  # Retorna None se não conseguiu receber a resposta

# Função para processar e formatar o comando digitado pelo usuário
def processar_comando(comando):
    partes_comando = comando.split()  # Divide o comando em partes com base nos espaços
    # Comando para criar uma tarefa
    if partes_comando[0].lower() == "criar" and len(partes_comando) >= 3:
        return f"criar|{partes_comando[1]}|{' '.join(partes_comando[2:])}"  # Formata o comando para enviar ao servidor
    # Comando para atualizar uma tarefa
    elif partes_comando[0].lower() == "atualizar" and len(partes_comando) >= 4:
        return f"atualizar|{partes_comando[1]}|{partes_comando[2]}|{' '.join(partes_comando[3:])}"
    # Comando para deletar uma tarefa
    elif partes_comando[0].lower() == "deletar" and len(partes_comando) == 2:
        return f"deletar|{partes_comando[1]}"
    # Comando para ler uma tarefa ou todas
    elif partes_comando[0].lower() == "ler":
        if len(partes_comando) == 2:  # Se foi especificado um ID
            return f"ler|{partes_comando[1]}"
        else:  # Se não foi especificado ID, lê todas as tarefas
            return "ler"
    else:
        print("Comando inválido. Tente novamente.")  # Se o comando não é reconhecido, imprime uma mensagem de erro
        return None

# Função principal que inicia o cliente
def iniciar_cliente():
    cliente_socket = conectar_ao_servidor()  # Estabelece a conexão com o servidor
    if not cliente_socket:  # Se não conseguiu conectar, termina a função
        return

    # Exibe os comandos disponíveis ao usuário
    print("Comandos disponíveis: criar <nome> <descrição>, ler [id], atualizar <id> <nome> <descrição>, deletar <id>")
    print("Digite 'sair' para encerrar o cliente.")

    # Loop para o cliente enviar comandos ao servidor
    while True:
        comando = input("\nDigite o comando: ").strip()  # Solicita o comando do usuário

        if comando.lower() == 'sair':  # Se o usuário digitar 'sair', encerra a conexão
            print("Encerrando a conexão...")
            break

        if not comando:  # Se o comando estiver vazio, pede para tentar novamente
            print("Comando vazio! Tente novamente.")
            continue

        comando_processado = processar_comando(comando)  # Processa o comando do usuário
        if not comando_processado:  # Se o comando for inválido, volta para o início do loop
            continue

        if not enviar_comando(cliente_socket, comando_processado):  # Envia o comando ao servidor
            break  # Se houve erro ao enviar, encerra o loop

        resposta = receber_resposta(cliente_socket)  # Recebe a resposta do servidor
        if resposta:
            print(f"Resposta do servidor: {resposta}")  # Exibe a resposta do servidor
        else:
            break  # Se não há resposta, encerra o loop

    cliente_socket.close()  # Fecha o socket do cliente

# Ponto de entrada do programa
if __name__ == "__main__":
    iniciar_cliente()  # Inicia o cliente quando o script é executado
