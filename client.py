import socket
from network_utils import enviar_comando, receber_resposta
from command_processor import processar_comando
from history_manager import GerenciadorHistorico

def interpretar_status(codigo_status: str) -> str:
    """
    Converte o código de status em uma mensagem compreensível para o usuário.

    Args:
        codigo_status (str): O código de status recebido do servidor.

    Returns:
        str: A mensagem correspondente ao código de status.
    """
    status = {
        "200": "Operação realizada com sucesso.",
        "201": "Tarefa criada com sucesso.",
        "202": "Tarefa atualizada com sucesso.",
        "203": "Tarefa lida com sucesso.",
        "204": "Tarefa excluída com sucesso.",
        "205": "Nenhuma tarefa foi criada ainda.",
        "300": "Tarefa não encontrada.",
        "400": "Erro na requisição.",
        "404": "Tarefa não existe."
    }
    return status.get(codigo_status, "Erro desconhecido.")

def receber_resposta(cliente_socket: socket.socket) -> str:
    """
    Recebe a resposta do servidor após o envio do comando.

    Args:
        cliente_socket (socket.socket): Socket da conexão com o servidor.

    Returns:
        str: A resposta recebida do servidor ou uma mensagem de erro.
    """
    try:
        resposta = cliente_socket.recv(1024).decode()
        return resposta
    except ConnectionResetError:
        print("Erro: Conexão com o servidor foi encerrada.")
    except Exception as e:
        print(f"Erro ao receber resposta: {e}")
    return None

def conectar_ao_servidor() -> socket.socket:
    """
    Estabelece a conexão com o servidor.

    Returns:
        socket.socket: O socket conectado ao servidor.
    """
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

def mostrar_comandos() -> None:
    """
    Exibe a lista de comandos disponíveis.
    """
    print("""
    Comandos disponíveis:
    1. criar: Cria uma nova tarefa.
    2. ler: Lê uma tarefa específica.
    3. atualizar: Atualiza uma tarefa existente.
    4. deletar: Exclui uma tarefa.
    5. historico: Exibe o histórico de comandos.
    6. comandos: Mostra novamente esta tabela de comandos.
    7. sair: Encerra o cliente.
    """)

def iniciar_cliente() -> None:
    """
    Função principal que gerencia a interação do cliente com o servidor.

    Returns:
        None
    """
    cliente_socket = conectar_ao_servidor()
    if not cliente_socket:
        return

    gerenciador_historico = GerenciadorHistorico()

    mostrar_comandos()

    while True:
        comando = input("\nDigite o comando: ").strip()

        if comando.lower() == 'sair':
            print("Encerrando a conexão...")
            break

        if comando.lower() == 'historico':
            gerenciador_historico.exibir_historico()
            continue

        if comando.lower() == 'comandos':
            mostrar_comandos()
            continue

        # Processa o comando e envia ao servidor
        comando_processado = processar_comando(comando)
        if not comando_processado:
            continue

        # Verifica a resposta antes de solicitar o ID
        if comando.lower() in ['ler', 'atualizar', 'deletar']:
            if not enviar_comando(cliente_socket, comando_processado):
                break
            resposta = receber_resposta(cliente_socket)

            if resposta:
                codigo_status, mensagem = resposta.split("|", 1)
                if codigo_status == "205":  # Nenhuma tarefa criada
                    print(interpretar_status(codigo_status))
                    continue  # Não pede o ID se não houver tarefas criadas

        if not enviar_comando(cliente_socket, comando_processado):
            break

        resposta = receber_resposta(cliente_socket)
        if resposta:
            codigo_status, mensagem = resposta.split("|", 1)
            mensagem_interpretada = interpretar_status(codigo_status)
            print(mensagem_interpretada)
            if mensagem:
                print(mensagem)  # Exibe apenas a mensagem adicional se houver
            gerenciador_historico.adicionar_ao_historico(comando_processado)

    cliente_socket.close()

if __name__ == "__main__":
    iniciar_cliente()
