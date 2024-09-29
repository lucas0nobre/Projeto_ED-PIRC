from threading import Lock
from estruturas.ListaEncadeada import Lista
from estruturas.dicionário import HashTable

class Tarefa:
    """
    Classe que define uma tarefa com ID, nome e descrição.

    Attributes:
        id_tarefa (int): ID único da tarefa.
        nome (str): Nome da tarefa.
        descricao (str): Descrição da tarefa.
    """
    def __init__(self, id_tarefa, nome, descricao):
        self.id_tarefa = id_tarefa
        self.nome = nome
        self.descricao = descricao

class GerenciadorTarefas:
    """
    Classe responsável por gerenciar tarefas, utilizando uma tabela hash personalizada.
    A classe suporta criação, leitura, atualização e exclusão de tarefas, além de manter um histórico de comandos.

    Attributes:
        tarefas (HashTable): Armazena as tarefas utilizando uma tabela hash.
        trava (Lock): Garante a sincronização entre threads.
        contador (int): Contador para gerar IDs únicos.
        historico (Lista): Armazena o histórico de comandos executados.
    """
    def __init__(self):
        self.tarefas = HashTable()  # Utiliza tabela hash personalizada
        self.trava = Lock()  # Lock para evitar concorrência
        self.contador = 0  # Contador para gerar IDs únicos
        self.historico = Lista()  # Lista encadeada para armazenar o histórico de comandos

    def criar_tarefa(self, nome, descricao):
        """
        Cria uma nova tarefa com um nome e descrição fornecidos.

        Args:
            nome (str): Nome da tarefa.
            descricao (str): Descrição da tarefa.

        Returns:
            int: O ID da tarefa criada.
        """
        with self.trava:
            self.contador += 1
            tarefa = Tarefa(self.contador, nome, descricao)
            self.tarefas.put(self.contador, tarefa)
            self.historico.append(f"criar|{nome}|{descricao}")
            return self.contador

    def ler_tarefa(self, id_tarefa=None):
        """
        Lê uma tarefa específica pelo ID ou retorna todas as tarefas.

        Args:
            id_tarefa (int, optional): ID da tarefa a ser lida. Defaults to None.

        Returns:
            Tarefa ou lista de tarefas: Retorna a tarefa específica ou todas as tarefas.
        """
        if id_tarefa:
            try:
                return self.tarefas.get(id_tarefa)
            except KeyError:
                return None
        return self.tarefas.items()

    def atualizar_tarefa(self, id_tarefa, nome, descricao):
        """
        Atualiza o nome e a descrição de uma tarefa existente.

        Args:
            id_tarefa (int): ID da tarefa a ser atualizada.
            nome (str): Novo nome da tarefa.
            descricao (str): Nova descrição da tarefa.

        Returns:
            bool: True se a tarefa foi atualizada, False caso contrário.
        """
        with self.trava:
            if id_tarefa in self.tarefas:
                tarefa = self.tarefas.get(id_tarefa)
                tarefa.nome = nome
                tarefa.descricao = descricao
                self.tarefas.put(id_tarefa, tarefa)
                self.historico.append(f"atualizar|{id_tarefa}|{nome}|{descricao}")
                return True
            return False

    def excluir_tarefa(self, id_tarefa):
        """
        Exclui uma tarefa com base no ID fornecido.

        Args:
            id_tarefa (int): ID da tarefa a ser excluída.

        Returns:
            bool: True se a tarefa foi excluída, False caso contrário.
        """
        with self.trava:
            if id_tarefa in self.tarefas:
                self.tarefas.remove(id_tarefa)
                self.historico.append(f"deletar|{id_tarefa}")
                return True
            return False

    def ler_historico(self):
        """
        Retorna o histórico de comandos executados.

        Returns:
            list: Lista com os comandos executados.
        """
        return list(self.historico)
