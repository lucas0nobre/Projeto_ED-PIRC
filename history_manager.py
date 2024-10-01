from estruturas.ListaEncadeada import Lista

class GerenciadorHistorico:
    """
    Classe responsável por gerenciar o histórico de comandos do cliente.
    
    Attributes:
        historico (Lista): Lista encadeada que armazena os comandos.
    """
    def __init__(self) -> None:
        self.historico = Lista()

    def adicionar_ao_historico(self, comando: str) -> None:
        """
        Adiciona um comando ao histórico.

        Args:
            comando (str): O comando a ser armazenado no histórico.
        """
        self.historico.append(comando)

    def exibir_historico(self) -> None:
        """
        Exibe o histórico de comandos em formato numerado.

        Returns:
            None
        """
        if len(self.historico) == 0:
            print("Histórico vazio.")
        else:
            print("Histórico de Comandos:")
            for i, cmd in enumerate(self.historico):
                print(f"{i + 1}. {cmd}")
