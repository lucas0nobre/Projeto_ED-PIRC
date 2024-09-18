import socket  # Biblioteca para comunicação de rede
import threading  # Biblioteca para trabalhar com múltiplas threads (concorrência)

# Classe que define uma tarefa
class Tarefa:
    def __init__(self, id_tarefa, nome, descricao):
        self.id_tarefa = id_tarefa  # ID único da tarefa
        self.nome = nome  # Nome da tarefa
        self.descricao = descricao  # Descrição da tarefa

# Classe para gerenciar as tarefas, usando um dicionário
class GerenciadorTarefas:
    def __init__(self):
        self.tarefas = {}  # Dicionário para armazenar as tarefas com ID como chave
        self.trava = threading.Lock()  # Lock para evitar problemas de concorrência entre threads
        self.contador = 0  # Contador para gerar IDs únicos para as tarefas
    
    # Método para criar uma nova tarefa
    def criar_tarefa(self, nome, descricao):
        with self.trava:  # Garante que apenas uma thread por vez executa essa parte do código
            self.contador += 1  # Incrementa o ID da próxima tarefa
            tarefa = Tarefa(self.contador, nome, descricao)  # Cria a tarefa
            self.tarefas[self.contador] = tarefa  # Adiciona a tarefa ao dicionário
            return self.contador  # Retorna o ID da tarefa criada

    # Método para ler uma tarefa específica ou todas as tarefas
    def ler_tarefa(self, id_tarefa=None):
        if id_tarefa:  # Se um ID foi fornecido, retorna a tarefa correspondente
            return self.tarefas.get(id_tarefa, None)  # Retorna a tarefa ou None se não encontrada
        return self.tarefas.values()  # Se nenhum ID foi fornecido, retorna todas as tarefas

    # Método para atualizar uma tarefa existente
    def atualizar_tarefa(self, id_tarefa, nome, descricao):
        with self.trava:  # Garante que a operação seja segura entre threads
            if id_tarefa in self.tarefas:  # Verifica se a tarefa existe
                tarefa = self.tarefas[id_tarefa]  # Recupera a tarefa
                tarefa.nome = nome  # Atualiza o nome da tarefa
                tarefa.descricao = descricao  # Atualiza a descrição da tarefa
                return True  # Retorna True se a tarefa foi atualizada
            return False  # Retorna False se a tarefa não foi encontrada

    # Método para excluir uma tarefa
    def excluir_tarefa(self, id_tarefa):
        with self.trava:  # Garante que a exclusão seja segura entre threads
            if id_tarefa in self.tarefas:  # Verifica se a tarefa existe
                del self.tarefas[id_tarefa]  # Remove a tarefa do dicionário
                return True  # Retorna True se a tarefa foi excluída
            return False  # Retorna False se a tarefa não foi encontrada

# Função para processar as requisições enviadas pelo cliente
def processar_requisicao(requisicao, gerenciador_tarefas):
    partes = requisicao.split("|")  # Divide a requisição por "|", que separa o comando dos parâmetros
    comando = partes[0].lower()  # Obtém o comando (criar, ler, atualizar, excluir)

    try:
        # Comando para criar uma nova tarefa
        if comando == "criar":
            nome_tarefa = partes[1]  # Obtém o nome da tarefa
            descricao = partes[2]  # Obtém a descrição da tarefa
            id_tarefa = gerenciador_tarefas.criar_tarefa(nome_tarefa, descricao)  # Cria a tarefa
            return f"Tarefa criada com ID: {id_tarefa}"  # Retorna o ID da tarefa criada
        
        # Comando para ler uma tarefa ou todas as tarefas
        elif comando == "ler":
            if len(partes) > 1:  # Verifica se um ID foi fornecido
                id_tarefa = int(partes[1])  # Converte o ID para inteiro
                tarefa = gerenciador_tarefas.ler_tarefa(id_tarefa)  # Lê a tarefa
                if tarefa:
                    return f"Tarefa {id_tarefa}: {tarefa.nome} - {tarefa.descricao}"  # Retorna os detalhes da tarefa
                else:
                    return "Tarefa não encontrada"  # Tarefa não foi encontrada
            else:
                tarefas = gerenciador_tarefas.ler_tarefa()  # Lê todas as tarefas
                return "\n".join([f"{tarefa.id_tarefa}: {tarefa.nome}" for tarefa in tarefas])  # Retorna a lista de tarefas
        
        # Comando para atualizar uma tarefa
        elif comando == "atualizar":
            id_tarefa = int(partes[1])  # Obtém o ID da tarefa
            nome_tarefa = partes[2]  # Obtém o novo nome
            descricao = partes[3]  # Obtém a nova descrição
            if gerenciador_tarefas.atualizar_tarefa(id_tarefa, nome_tarefa, descricao):
                return "Tarefa atualizada com sucesso"  # Retorna confirmação de sucesso
            else:
                return "Tarefa não encontrada"  # Tarefa não foi encontrada
        
        # Comando para excluir uma tarefa
        elif comando == "excluir":
            id_tarefa = int(partes[1])  # Obtém o ID da tarefa
            if gerenciador_tarefas.excluir_tarefa(id_tarefa):
                return "Tarefa excluída com sucesso"  # Retorna confirmação de exclusão
            else:
                return "Tarefa não encontrada"  # Tarefa não foi encontrada
        
        else:
            return "Comando inválido"  # Comando desconhecido

    # Tratamento de exceção caso os parâmetros sejam insuficientes
    except IndexError:
        return "Erro: parâmetros insuficientes"
    # Tratamento de exceção caso o ID não seja um número
    except ValueError:
        return "Erro: ID da tarefa deve ser um número"

# Função que lida com cada cliente individualmente
def lidar_com_cliente(conn, addr, gerenciador_tarefas):
    print(f"Conectado por {addr}")  # Exibe o endereço do cliente conectado
    try:
        while True:
            dados = conn.recv(1024).decode()  # Recebe dados do cliente
            if not dados:
                break  # Sai do loop se não houver mais dados
            resposta = processar_requisicao(dados, gerenciador_tarefas)  # Processa a requisição
            conn.sendall(resposta.encode())  # Envia a resposta de volta para o cliente
    except ConnectionResetError:
        print(f"Conexão com {addr} foi interrompida")  # Lida com erro de conexão interrompida
    except Exception as e:
        print(f"Erro ao lidar com cliente {addr}: {e}")  # Captura outros erros
    finally:
        conn.close()  # Fecha a conexão com o cliente
        print(f"Conexão com {addr} encerrada")  # Exibe mensagem ao encerrar a conexão

# Função que inicia o servidor
def iniciar_servidor():
    gerenciador_tarefas = GerenciadorTarefas()  # Cria uma instância do gerenciador de tarefas
    
    try:
        # Cria um socket de servidor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
            servidor_socket.bind(('localhost', 65432))  # Define o endereço e porta do servidor
            servidor_socket.listen()  # Coloca o servidor em modo de escuta
            print("Servidor em execução...")
            
            while True:
                conn, addr = servidor_socket.accept()  # Aceita conexões de clientes
                # Cria uma nova thread para cada cliente
                thread_cliente = threading.Thread(target=lidar_com_cliente, args=(conn, addr, gerenciador_tarefas))
                thread_cliente.daemon = True  # Define a thread como daemon (encerra ao finalizar o processo)
                thread_cliente.start()  # Inicia a thread para lidar com o cliente
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")  # Captura erros ao iniciar o servidor

# Ponto de entrada do programa
if __name__ == "__main__":
    iniciar_servidor()  # Inicia o servidor quando o script é executado
