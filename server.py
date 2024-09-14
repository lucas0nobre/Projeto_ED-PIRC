import socket
import threading

# Classe que define uma tarefa
class Tarefa:
    def __init__(self, id_tarefa, nome, descricao):
        self.id_tarefa = id_tarefa
        self.nome = nome
        self.descricao = descricao

# Classe para gerenciar as tarefas (usando um dicionário)
class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = {}  # Dicionário para armazenar as tarefas
        self.trava = threading.Lock()  # Lock para evitar condições de corrida
        self.contador = 0  # Contador de IDs de tarefas
    
    # Método para criar uma nova tarefa
    def criar_tarefa(self, nome, descricao):
        with self.trava:  # Garante que apenas uma thread acesse o bloco por vez
            self.contador += 1
            tarefa = Tarefa(self.contador, nome, descricao)
            self.tarefas[self.contador] = tarefa
            return self.contador

    # Método para ler uma tarefa ou todas as tarefas
    def ler_tarefa(self, id_tarefa=None):
        if id_tarefa:
            return self.tarefas.get(id_tarefa, None)
        return self.tarefas.values()

    # Método para atualizar uma tarefa existente
    def atualizar_tarefa(self, id_tarefa, nome, descricao):
        with self.trava:
            if id_tarefa in self.tarefas:
                tarefa = self.tarefas[id_tarefa]
                tarefa.nome = nome
                tarefa.descricao = descricao
                return True
            return False

    # Método para excluir uma tarefa
    def excluir_tarefa(self, id_tarefa):
        with self.trava:
            if id_tarefa in self.tarefas:
                del self.tarefas[id_tarefa]
                return True
            return False

# Função para lidar com cada cliente
def lidar_com_cliente(conn, addr, gerenciador_tarefas):
    print(f"Conectado por {addr}")
    try:
        while True:
            try:
                dados = conn.recv(1024).decode()  # Recebe dados do cliente
                if not dados:
                    break

                # Processa a requisição do cliente e envia a resposta
                resposta = processar_requisicao(dados, gerenciador_tarefas)
                conn.sendall(resposta.encode())  # Envia resposta para o cliente
            
            except ConnectionResetError:
                print(f"Conexão com {addr} foi interrompida")
                break  # Encerra o loop se a conexão for fechada abruptamente
    except Exception as e:
        print(f"Erro ao lidar com cliente {addr}: {e}")
    finally:
        conn.close()  # Garante que a conexão será fechada
        print(f"Conexão com {addr} encerrada")

# Função para processar a requisição do cliente
def processar_requisicao(requisicao, gerenciador_tarefas):
    partes = requisicao.split("|")
    comando = partes[0].lower()

    try:
        if comando == "criar":
            nome_tarefa = partes[1]
            descricao = partes[2]
            id_tarefa = gerenciador_tarefas.criar_tarefa(nome_tarefa, descricao)
            return f"Tarefa criada com ID: {id_tarefa}"
        
        elif comando == "ler":
            if len(partes) > 1:
                id_tarefa = int(partes[1])
                tarefa = gerenciador_tarefas.ler_tarefa(id_tarefa)
                if tarefa:
                    return f"Tarefa {id_tarefa}: {tarefa.nome} - {tarefa.descricao}"
                else:
                    return "Tarefa não encontrada"
            else:
                tarefas = gerenciador_tarefas.ler_tarefa()
                return "\n".join([f"{tarefa.id_tarefa}: {tarefa.nome}" for tarefa in tarefas])
        
        elif comando == "atualizar":
            id_tarefa = int(partes[1])
            nome_tarefa = partes[2]
            descricao = partes[3]
            if gerenciador_tarefas.atualizar_tarefa(id_tarefa, nome_tarefa, descricao):
                return "Tarefa atualizada com sucesso"
            else:
                return "Tarefa não encontrada"
        
        elif comando == "excluir":
            id_tarefa = int(partes[1])
            if gerenciador_tarefas.excluir_tarefa(id_tarefa):
                return "Tarefa excluída com sucesso"
            else:
                return "Tarefa não encontrada"
        
        else:
            return "Comando inválido"

    except IndexError:
        return "Erro: parâmetros insuficientes"
    except ValueError:
        return "Erro: ID da tarefa deve ser um número"

# Função para iniciar o servidor
def iniciar_servidor():
    gerenciador_tarefas = GerenciadorTarefas()  # Instancia o gerenciador de tarefas
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind(('localhost', 65432))  # Define o endereço e a porta do servidor
        servidor_socket.listen()  # Coloca o servidor em estado de escuta
        print("Servidor em execução...")
        
        while True:
            conn, addr = servidor_socket.accept()  # Aceita uma conexão
            thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conn, addr, gerenciador_tarefas))
            thread_cliente.daemon = True  # Garante que a thread será finalizada ao encerrar o processo
            thread_cliente.start()  # Cria e inicia uma nova thread para cada cliente

# Ponto de entrada do programa
if __name__ == "__main__":
    iniciar_servidor()
