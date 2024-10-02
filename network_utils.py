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
        cliente_socket.sendall(comando.encode())
        return True
    except BrokenPipeError:
        print("Erro: Conexão com o servidor foi perdida.")
        return False
    except Exception as e:
        print(f"Erro ao enviar comando: {e}")
        return False

def receber_resposta(cliente_socket: socket.socket) -> None:
    """
    Recebe a resposta do servidor após o envio do comando.

    Args:
        cliente_socket (socket.socket): Socket da conexão com o servidor.

    Returns:
        None
    """
    try:
        resposta = cliente_socket.recv(1024).decode()
        codigo_status, mensagem = resposta.split("|", 1)
        print(f"{interpretar_status(codigo_status)}: {mensagem}")
    except ConnectionResetError:
        print("Erro: Conexão com o servidor foi encerrada.")
    except Exception as e:
        print(f"Erro ao receber resposta: {e}")

def interpretar_status(codigo_status: str) -> str:
    """
    Converte o código de status em uma mensagem compreensível para o usuário.

    Args:
        codigo_status (str): O código de status recebido do servidor.

    Returns:
        str: A mensagem correspondente ao código de status.
    """
    status = {
        "200": "Sucesso",
        "400": "Erro na requisição",
        "404": "Não encontrado",
        "500": "Erro interno do servidor"
    }
    return status.get(codigo_status, "Código de status desconhecido")
