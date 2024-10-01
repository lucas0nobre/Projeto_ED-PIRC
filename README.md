# Projeto_ED-PIRC
Sistema de gerenciamento de tarefas

Felipe Antonio Ramalho Macedo
felipe.macedo@academico.ifpb.edu.br

estruturas de dados e protocolos de redes

alex sandro e leonidas francisco


Descrição do Problema
O Sistema de Gerenciamento de Tarefas é uma aplicação distribuída que segue o modelo cliente/servidor. O cenário envolve múltiplos usuários, ou clientes, que se conectam a um servidor centralizado para criar, consultar, atualizar e excluir tarefas em um ambiente colaborativo.

A comunicação entre cliente e servidor é realizada via sockets, utilizando um protocolo de aplicação personalizado para o projeto. O servidor gerencia várias conexões simultâneas e mantém um histórico de comandos, garantindo que todas as operações sejam armazenadas e processadas corretamente.

Funcionalidades:
Criação de Tarefas: Clientes podem criar novas tarefas fornecendo um nome e descrição.
Consulta de Tarefas: Clientes podem listar todas as tarefas ou consultar uma tarefa específica.
Atualização de Tarefas: Modificação de nome e descrição de uma tarefa existente.
Exclusão de Tarefas: Remover uma tarefa com base no seu ID.
Histórico: Visualizar o histórico de comandos executados.
Arquivos do Projeto
Nome do Arquivo	Descrição
client.py	Implementa o cliente, responsável por enviar comandos ao servidor.
server.py	Implementa o servidor, gerencia as conexões e tarefas.
gerenciador_tarefas.py	Gerencia todas as operações relacionadas às tarefas (criação, leitura, etc).
network_utils.py	Contém funções auxiliares de rede como enviar comandos e receber respostas.
history_manager.py	Gerencia o histórico de comandos dos clientes.
ListaEncadeada.py	Implementa uma lista encadeada usada para o histórico.
dicionário.py	Implementa uma tabela hash personalizada para armazenar tarefas.
README.md	Arquivo de descrição do projeto.
Pré-requisitos para Execução
Python 3.x: O projeto é desenvolvido em Python, então você precisará de uma versão recente do Python instalada.
Bibliotecas padrão do Python:
socket: Para a comunicação cliente-servidor.
threading: Para permitir o servidor lidar com várias conexões simultâneas.
Instalação do Python
Para instalar o Python, siga as instruções para o seu sistema operacional:

Windows: Download do Python
Linux: Use o gerenciador de pacotes da sua distribuição (apt-get, yum, etc.).
MacOS: Utilize o brew install python ou baixe diretamente do site do Python.
Protocolo da Aplicação
A comunicação entre o cliente e o servidor segue um protocolo simples baseado em mensagens de texto. Abaixo está a documentação dos comandos aceitos:

Comandos do Cliente
Criar Tarefa:

Formato: criar|<nome>|<descrição>
Parâmetros:
<nome>: Nome da tarefa.
<descrição>: Descrição da tarefa.
Resposta: Tarefa criada com ID: <id_tarefa>
Ler Tarefa:

Formato:
ler|<id_tarefa>: Lê uma tarefa específica pelo ID.
ler: Lê todas as tarefas.
Resposta:
Tarefa <id_tarefa>: <nome> - <descrição>
Ou uma lista de tarefas, se o comando ler for utilizado sem o ID.
Atualizar Tarefa:

Formato: atualizar|<id_tarefa>|<novo_nome>|<nova_descricao>
Parâmetros:
<id_tarefa>: ID da tarefa a ser atualizada.
<novo_nome>: Novo nome da tarefa.
<nova_descricao>: Nova descrição da tarefa.
Resposta: Tarefa atualizada com sucesso ou Tarefa não encontrada.
Excluir Tarefa:

Formato: deletar|<id_tarefa>
Parâmetros:
<id_tarefa>: ID da tarefa a ser excluída.
Resposta: Tarefa excluída com sucesso ou Tarefa não encontrada.
Histórico:

Formato: historico
Resposta: Retorna a lista de comandos executados ou "Nenhum comando registrado".

Instruções para execução:

Executar o Servidor
Abrir um terminal: Navegue até a pasta onde você salvou os arquivos do projeto.

Iniciar o servidor: No terminal, execute o seguinte comando para iniciar o servidor:
python server.py

O servidor agora estará em execução, esperando conexões de clientes. Ele ficará escutando na porta 65432 por novas requisições.

Executar o Cliente
Abrir um novo terminal: Em outra janela de terminal, navegue novamente até a pasta do projeto.

Iniciar o cliente: No terminal, execute o seguinte comando para iniciar o cliente:

python client.py


Utilizar o Cliente
Com o cliente em execução, você pode interagir com o servidor digitando comandos conforme descrito na seção "Protocolo da Aplicação" do README. Por exemplo:

Para criar uma nova tarefa: criar|Tarefa1|Descrição da tarefa
Para listar todas as tarefas: ler
Para atualizar uma tarefa: atualizar|1|Novo Nome|Nova descrição
Para excluir uma tarefa: deletar|1
Para ver o histórico de comandos: historico
Para encerrar a sessão do cliente, digite o comando:

sair

 Encerrar o Servidor
O servidor continuará em execução até que você o interrompa manualmente. Para interromper o servidor, vá ao terminal onde o servidor está rodando e pressione Ctrl + C. Isso irá parar o servidor e encerrar todas as conexões.

