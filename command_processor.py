def processar_comando(comando: str) -> str:
    """
    Processa o comando digitado pelo usuário e o formata de acordo com o protocolo esperado pelo servidor.

    Args:
        comando (str): O comando digitado pelo usuário.

    Returns:
        str: O comando formatado ou None se o comando for inválido.
    """
    if comando.lower() == "criar":
        nome_tarefa = input("Digite o nome da tarefa: ")
        descricao = input("Digite a descrição da tarefa: ")
        return f"criar|{nome_tarefa}|{descricao}"

    elif comando.lower() == "atualizar":
        id_tarefa = input("Digite o ID da tarefa: ")
        nome_tarefa = input("Digite o novo nome da tarefa: ")
        descricao = input("Digite a nova descrição da tarefa: ")
        return f"atualizar|{id_tarefa}|{nome_tarefa}|{descricao}"

    elif comando.lower() == "ler":
        id_tarefa = input("Digite o ID da tarefa: ")
        return f"ler|{id_tarefa}"

    elif comando.lower() == "deletar":
        id_tarefa = input("Digite o ID da tarefa: ")
        return f"deletar|{id_tarefa}"

    else:
        print("Comando inválido.")
        return None
