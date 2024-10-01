import socket  # Biblioteca para comunicação em rede
from typing import Optional
from estruturas.ListaEncadeada import Lista  # Importa a lista duplamente encadeada
from network_utils import enviar_comando, receber_resposta  # Funções de rede
from command_processor import processar_comando  # Função para processar e validar comandos
from history_manager import GerenciadorHistorico  # Gerenciamento do histórico de comandos

# Função para estabelecer a conexão com o servidor
def conectar_ao_servidor() -> Optional[socket.socket]:
    """
    Tenta se conectar ao servidor em 'localhost' na porta 65432.
    
    Returns:
        Optional[socket.socket]: Retorna o objeto socket se a conexão for bem-sucedida,
        ou None se houver algum erro de conexão.
    """
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect(('localhost', 65432))  # Conectando ao servidor no localhost
        print("Cliente conectado ao servidor.")
        return cliente_socket
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está em execução.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

# Função principal que inicia o cliente
def iniciar_cliente() -> None:
    """
    Função principal que gerencia a conexão com o servidor, processa os comandos,
    mantém o histórico e exibe as respostas recebidas do servidor.
    
    Returns:
        None
    """
    cliente_socket = conectar_ao_servidor()
    if not cliente_socket:
        return  # Sai se não conseguir conectar ao servidor

    gerenciador_historico = GerenciadorHistorico()  # Inicializa o gerenciador de histórico

    print("Comandos disponíveis: criar <nome> <descrição>, ler [id], atualizar <id> <nome> <descrição>, deletar <id>")
    print("Digite 'sair' para encerrar o cliente.")
    print("Digite 'historico' para ver os comandos enviados.")

    while True:
        comando = input("\nDigite o comando: ").strip()

        if comando.lower() == 'sair':
            print("Encerrando a conexão...")
            break  # Sai do loop se o usuário digitar 'sair'

        if comando.lower() == 'historico':
            # Exibe o histórico de comandos
            gerenciador_historico.exibir_historico()
            continue

        if not comando:
            print("Comando vazio! Tente novamente.")
            continue

        comando_processado = processar_comando(comando)
        if not comando_processado:
            continue

        if not enviar_comando(cliente_socket, comando_processado):
            break  # Sai do loop se não conseguir enviar o comando

        resposta = receber_resposta(cliente_socket)
        if resposta:
            print(f"Resposta do servidor: {resposta}")
            # Armazena o comando no histórico
            gerenciador_historico.adicionar_ao_historico(comando_processado)
        else:
            break  # Sai do loop se a resposta for None

    cliente_socket.close()

# Ponto de entrada do programa
if __name__ == "__main__":
    iniciar_cliente()
