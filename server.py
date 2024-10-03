import socket
import threading
import os

from gerenciador_tarefas import GerenciadorTarefas

# Adicionar configuração para SSH
def configurar_ssh():
    os.system("sudo service ssh start")  # Inicia o servidor SSH
    print("Servidor SSH em execução...")
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
            resposta = f"201|Tarefa criada com sucesso. ID: {id_tarefa}"
        
        elif comando == "ler":
            id_tarefa = int(partes[1])
            tarefa = gerenciador_tarefas.ler_tarefa(id_tarefa)
            if tarefa:
                resposta = f"203|Tarefa lida com sucesso. {tarefa.nome} - {tarefa.descricao}"
            else:
                resposta = "300|Tarefa não encontrada."

        elif comando == "atualizar":
            id_tarefa = int(partes[1])
            nome_tarefa = partes[2]
            descricao = partes[3]
            if gerenciador_tarefas.atualizar_tarefa(id_tarefa, nome_tarefa, descricao):
                resposta = "202|Tarefa atualizada com sucesso."
            else:
                resposta = "404|Tarefa não existe."
        
        elif comando == "deletar":
            id_tarefa = int(partes[1])
            if gerenciador_tarefas.excluir_tarefa(id_tarefa):
                resposta = "204|Tarefa excluída com sucesso."
            else:
                resposta = "404|Tarefa não existe."
        
        elif comando == "historico":
            historico = gerenciador_tarefas.ler_historico()
            resposta = "200|" + ("\n".join(historico) if historico else "Nenhum comando registrado.")

        else:
            resposta = "400|Comando inválido."
    
    except IndexError:
        resposta = "400|Erro: parâmetros insuficientes."
    except ValueError:
        resposta = "400|Erro: ID da tarefa deve ser um número."

    return resposta


def lidar_com_cliente(conn: socket.socket, addr: tuple) -> None:
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

def iniciar_servidor() -> None:
    # Configurando IP e SSH no servidor
    configurar_ssh()  # Inicia o serviço SSH
    ip_servidor = '0.0.0.0'  # Exemplo de IP estático para o servidor
    porta = 9999
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
            servidor_socket.bind((ip_servidor, porta))
            servidor_socket.listen()
            print(f"Servidor em execução no IP {ip_servidor}:{porta}...")
            
            while True:
                conn, addr = servidor_socket.accept()
                thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
                thread_cliente.daemon = True
                thread_cliente.start()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    iniciar_servidor()
