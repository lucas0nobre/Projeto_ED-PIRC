import socket
from network_utils import enviar_comando, receber_resposta
from command_processor import processar_comando
from history_manager import GerenciadorHistorico

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
    2. ler <id>: Lê uma tarefa específica.
    3. atualizar <id>: Atualiza uma tarefa existente.
    4. deletar <id>: Exclui uma tarefa.
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

        if not comando:
            print("Comando vazio! Tente novamente.")
            continue

        comando_processado = processar_comando(comando)
        if not comando_processado:
            continue

        if not enviar_comando(cliente_socket, comando_processado):
            break

        receber_resposta(cliente_socket)
        gerenciador_historico.adicionar_ao_historico(comando_processado)

    cliente_socket.close()

if __name__ == "__main__":
    iniciar_cliente()
