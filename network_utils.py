import socket

def enviar_comando(cliente_socket: socket.socket, comando: str) -> bool:
    """
    Envia um comando do cliente ao servidor.

    Args:
        cliente_socket (socket.socket): Socket da conexão com o servidor.
        comando (str): O comando que será enviado ao servidor.

    Returns:
        bool: True se o comando foi enviado com sucesso, False se houve algum erro.
    """
    try:
        cliente_socket.sendall(comando.encode())  # Enviando o comando ao servidor
    except BrokenPipeError:
        print("Erro: Conexão com o servidor foi perdida.")
        return False
    except Exception as e:
        print(f"Erro ao enviar comando: {e}")
        return False
    return True

def receber_resposta(cliente_socket: socket.socket) -> str:
    """
    Recebe a resposta do servidor após o envio do comando.

    Args:
        cliente_socket (socket.socket): Socket da conexão com o servidor.

    Returns:
        str: A resposta recebida do servidor ou None se houver algum erro.
    """
    try:
        resposta = cliente_socket.recv(1024).decode()  # Recebendo resposta do servidor
        return resposta
    except ConnectionResetError:
        print("Erro: Conexão com o servidor foi encerrada.")
    except Exception as e:
        print(f"Erro ao receber resposta: {e}")
    return None
