import socket
import threading

# Classe que define uma tarefa
class Task:
    def __init__(self, task_id, name, description):
        self.task_id = task_id
        self.name = name
        self.description = description

# Classe para gerenciar as tarefas (usando um dicionário)
class TaskManager:
    def __init__(self):
        self.tasks = {}  # Dicionário para armazenar as tarefas
        self.lock = threading.Lock()  # Lock para evitar condições de corrida
        self.counter = 0  # Contador de IDs de tarefas
    
    # Método para criar uma nova tarefa
    def create_task(self, name, description):
        with self.lock:  # Garante que apenas uma thread acesse o bloco por vez
            self.counter += 1
            task = Task(self.counter, name, description)
            self.tasks[self.counter] = task
            return self.counter

    # Método para ler uma tarefa ou todas as tarefas
    def read_task(self, task_id=None):
        if task_id:
            return self.tasks.get(task_id, None)
        return self.tasks.values()

    # Método para atualizar uma tarefa existente
    def update_task(self, task_id, name, description):
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.name = name
                task.description = description
                return True
            return False

    # Método para excluir uma tarefa
    def delete_task(self, task_id):
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                return True
            return False

# Função para lidar com cada cliente
def handle_client(conn, addr, task_manager):
    print(f"Conectado por {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            # Processa a requisição do cliente e envia a resposta
            response = process_request(data, task_manager)
            conn.sendall(response.encode())
    finally:
        conn.close()

# Função para processar a requisição do cliente
def process_request(request, task_manager):
    parts = request.split("|")
    command = parts[0].upper()

    if command == "CREATE":
        task_name = parts[1]
        description = parts[2]
        task_id = task_manager.create_task(task_name, description)
        return f"Tarefa criada com ID: {task_id}"
    
    elif command == "READ":
        if len(parts) > 1:
            task_id = int(parts[1])
            task = task_manager.read_task(task_id)
            if task:
                return f"Tarefa {task_id}: {task.name} - {task.description}"
            else:
                return "Tarefa não encontrada"
        else:
            tasks = task_manager.read_task()
            return "\n".join([f"{task.task_id}: {task.name}" for task in tasks])
    
    elif command == "UPDATE":
        task_id = int(parts[1])
        task_name = parts[2]
        description = parts[3]
        if task_manager.update_task(task_id, task_name, description):
            return "Tarefa atualizada com sucesso"
        else:
            return "Tarefa não encontrada"
    
    elif command == "DELETE":
        task_id = int(parts[1])
        if task_manager.delete_task(task_id):
            return "Tarefa excluída com sucesso"
        else:
            return "Tarefa não encontrada"
    
    else:
        return "Comando inválido"

# Função para iniciar o servidor
def start_server():
    task_manager = TaskManager()  # Instancia o gerenciador de tarefas
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 65432))  # Define o endereço e a porta do servidor
        server_socket.listen()  # Coloca o servidor em estado de escuta
        print("Servidor em execução...")
        
        while True:
            conn, addr = server_socket.accept()  # Aceita uma conexão
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, task_manager))
            client_thread.start()  # Cria e inicia uma nova thread para cada cliente

# Ponto de entrada do programa
if __name__ == "__main__":
    start_server()
