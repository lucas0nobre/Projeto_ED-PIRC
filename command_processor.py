def processar_comando(comando: str):
    """
    Processa o comando digitado pelo usuário e o formata de acordo com o protocolo esperado pelo servidor.
    
    Args:
        comando (str): O comando digitado pelo usuário.
    
    Returns:
        Optional[str]: O comando formatado ou None se o comando for inválido.
    """
    partes_comando = comando.split()
    
    # Validação para o comando 'criar'
    if partes_comando[0].lower() == "criar":
        if len(partes_comando) < 3:
            print("Erro: O comando 'criar' requer um nome e uma descrição.")
            return None
        return f"criar|{partes_comando[1]}|{' '.join(partes_comando[2:])}"
    
    # Validação para o comando 'atualizar'
    elif partes_comando[0].lower() == "atualizar":
        if len(partes_comando) < 4:
            print("Erro: O comando 'atualizar' requer um ID, nome e descrição.")
            return None
        try:
            int(partes_comando[1])  # Valida se o ID é um número inteiro
        except ValueError:
            print("Erro: O ID da tarefa deve ser um número.")
            return None
        return f"atualizar|{partes_comando[1]}|{partes_comando[2]}|{' '.join(partes_comando[3:])}"
    
    # Validação para o comando 'deletar'
    elif partes_comando[0].lower() == "deletar":
        if len(partes_comando) != 2:
            print("Erro: O comando 'deletar' requer um ID.")
            return None
        try:
            int(partes_comando[1])  # Valida se o ID é um número inteiro
        except ValueError:
            print("Erro: O ID da tarefa deve ser um número.")
            return None
        return f"deletar|{partes_comando[1]}"
    
    # Validação para o comando 'ler'
    elif partes_comando[0].lower() == "ler":
        if len(partes_comando) == 2:
            try:
                int(partes_comando[1])  # Valida se o ID é um número inteiro
            except ValueError:
                print("Erro: O ID da tarefa deve ser um número.")
                return None
            return f"ler|{partes_comando[1]}"
        else:
            return "ler"
    
    else:
        print("Comando inválido. Tente novamente.")
        return None
