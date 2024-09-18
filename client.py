import socket  # Biblioteca para comunicação em rede
from ListaEncadeada import Lista  # Importa a lista duplamente encadeada

# Função para estabelecer a conexão com o servidor
def conectar_ao_servidor():
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 65432))
        print("Cliente conectado ao servidor.")
        return cliente_socket
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está em execução.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# Função para enviar comandos ao servidor
def enviar_comando(cliente_socket, comando):
    try:
        cliente_socket.sendall(comando.encode())
    except BrokenPipeError:
        print("Erro: Conexão com o servidor foi perdida.")
        return False
    except Exception as e:
        print(f"Erro ao enviar comando: {e}")
        return False
    return True

# Função para receber a resposta do servidor
def receber_resposta(cliente_socket):
    try:
        resposta = cliente_socket.recv(1024).decode()
        return resposta
    except ConnectionResetError:
        print("Erro: Conexão com o servidor foi encerrada.")
    except Exception as e:
        print(f"Erro ao receber resposta: {e}")
    return None

# Função para processar e formatar o comando digitado pelo usuário
def processar_comando(comando):
    partes_comando = comando.split()
    if partes_comando[0].lower() == "criar" and len(partes_comando) >= 3:
        return f"criar|{partes_comando[1]}|{' '.join(partes_comando[2:])}"
    elif partes_comando[0].lower() == "atualizar" and len(partes_comando) >= 4:
        return f"atualizar|{partes_comando[1]}|{partes_comando[2]}|{' '.join(partes_comando[3:])}"
    elif partes_comando[0].lower() == "deletar" and len(partes_comando) == 2:
        return f"deletar|{partes_comando[1]}"  # Mantido como 'deletar'
    elif partes_comando[0].lower() == "ler":
        if len(partes_comando) == 2:
            return f"ler|{partes_comando[1]}"
        else:
            return "ler"
    else:
        print("Comando inválido. Tente novamente.")
        return None

# Função principal que inicia o cliente
def iniciar_cliente():
    cliente_socket = conectar_ao_servidor()
    if not cliente_socket:
        return

    # Inicializa a lista duplamente encadeada para o histórico de comandos
    historico = Lista()

    print("Comandos disponíveis: criar <nome> <descrição>, ler [id], atualizar <id> <nome> <descrição>, deletar <id>")
    print("Digite 'sair' para encerrar o cliente.")

    while True:
        comando = input("\nDigite o comando: ").strip()

        if comando.lower() == 'sair':
            print("Encerrando a conexão...")
            break

        if not comando:
            print("Comando vazio! Tente novamente.")
            continue

        comando_processado = processar_comando(comando)
        if not comando_processado:
            continue

        if not enviar_comando(cliente_socket, comando_processado):
            break

        resposta = receber_resposta(cliente_socket)
        if resposta:
            print(f"Resposta do servidor: {resposta}")
            # Armazena o comando no histórico
            historico.append(comando_processado)
        else:
            break

    cliente_socket.close()

# Ponto de entrada do programa
if __name__ == "__main__":
    iniciar_cliente()
