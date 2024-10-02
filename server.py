import socket
import threading
from gerenciador_tarefas import GerenciadorTarefas

def processar_requisicao(requisicao: str, gerenciador_tarefas: GerenciadorTarefas) -> str:
    """
    Processa as requisições enviadas pelo cliente, baseadas no protocolo.

    Args:
        requisicao (str): Requisição do cliente no formato do protocolo.
        gerenciador_tarefas (GerenciadorTarefas): Instância do gerenciador de tarefas.

    Returns:
        str: Resposta com código de status e mensagem a ser enviada de volta ao cliente.
    """
    partes = requisicao.split("|")
    comando = partes[0].lower()

    # Verifica se não há nenhuma tarefa criada para comandos que exigem tarefas
    if comando in ['ler', 'atualizar', 'deletar']:
        if not gerenciador_tarefas.tarefas.items():
            return "205|Nenhuma tarefa foi criada ainda."

    try:
        if comando == "criar":
            nome_tarefa = partes[1]
            descricao = partes[2]
            id_tarefa = gerenciador_tarefas.criar_tarefa(nome_tarefa, descricao)
            return f"201|ID: {id_tarefa}"
        
        elif comando == "ler":
            id_tarefa = int(partes[1])
            tarefa = gerenciador_tarefas.ler_tarefa(id_tarefa)
            if tarefa:
                return f"203|{tarefa.nome} - {tarefa.descricao}"
            return "300|Tarefa não encontrada."

        elif comando == "atualizar":
            id_tarefa = int(partes[1])
            nome_tarefa = partes[2]
            descricao = partes[3]
            if gerenciador_tarefas.atualizar_tarefa(id_tarefa, nome_tarefa, descricao):
                return "202|"
            return "404|Tarefa não existe."
        
        elif comando == "deletar":
            id_tarefa = int(partes[1])
            if gerenciador_tarefas.excluir_tarefa(id_tarefa):
                return "204|"
            return "404|Tarefa não existe."
        
        elif comando == "historico":
            historico = gerenciador_tarefas.ler_historico()
            return "200|" + ("\n".join(historico) if historico else "Nenhum comando registrado.")

        return "400|Comando inválido."
    
    except IndexError:
        return "400|Erro: parâmetros insuficientes."
    except ValueError:
        return "400|Erro: ID da tarefa deve ser um número."

def lidar_com_cliente(conn: socket.socket, addr: tuple) -> None:
    """
    Lida com cada cliente individualmente, processando as requisições enviadas.

    Args:
        conn (socket.socket): Socket de comunicação com o cliente.
        addr (tuple): Endereço do cliente.
    """
    print(f"Conectado por {addr}")
    
    # Cada cliente terá seu próprio gerenciador de tarefas
    gerenciador_tarefas = GerenciadorTarefas()

    try:
        while True:
            dados = conn.recv(1024).decode()
            if not dados:
                break
            resposta = processar_requisicao(dados, gerenciador_tarefas)
            conn.sendall(resposta.encode())
    except Exception as e:
        print(f"Erro ao lidar com cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexão com {addr} encerrada")

def iniciar_servidor() -> None:
    """
    Inicia o servidor e fica em modo de escuta para aceitar conexões de clientes.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
            servidor_socket.bind(('localhost', 65432))
            servidor_socket.listen()
            print("Servidor em execução...")
            
            while True:
                conn, addr = servidor_socket.accept()
                # Cada cliente é tratado de forma independente em uma thread com seu gerenciador de tarefas
                thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
                thread_cliente.daemon = True
                thread_cliente.start()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    iniciar_servidor()
