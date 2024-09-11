# Projeto_ED-PIRC
Sistema de gerenciamento de tarefas

Felipe Antonio Ramalho Macedo
felipe.macedo@academico.ifpb.edu.br
Lucas Alves da Nobrega
alves.nobrega@academico.ifpb.edu.br

estruturas de dados e protocolos de redes

alex sandro e leonidas francisco

O Sistema de Gerenciamento de Tarefas é uma aplicação distribuída que segue o modelo cliente/servidor. O cenário envolve múltiplos usuários, ou clientes, que se conectam a um servidor centralizado para criar, consultar, atualizar e excluir tarefas em um ambiente colaborativo. A comunicação entre cliente e servidor é realizada via sockets, utilizando um protocolo de aplicação específico para este projeto.

Os serviços e funcionalidades contemplados pela aplicação são:

Criação de Tarefas: Os clientes podem criar novas tarefas, fornecendo um nome e uma descrição.
Consulta de Tarefas: Os clientes podem consultar uma tarefa específica ou listar todas as tarefas.
Atualização de Tarefas: É possível modificar o nome e a descrição de uma tarefa existente.
Exclusão de Tarefas: Os clientes podem remover uma tarefa do sistema.
O servidor deve gerenciar diversas conexões simultâneas, garantindo a integridade dos dados através de mecanismos de sincronização para evitar condições de corrida.


Arquivos do Projeto
Nome do Arquivo	Descrição
server.py	Implementa o servidor que gerencia as tarefas, processa as requisições dos clientes e mantém a lógica de negócio da aplicação, usando sockets e threads para atender várias conexões simultaneamente.
client.py	Implementa o cliente que se conecta ao servidor para enviar comandos de criação, consulta, atualização e exclusão de tarefas.
task.py	Contém a classe Task, que define a estrutura de uma tarefa no sistema, incluindo ID, nome e descrição.
task_manager.py	Implementa a classe TaskManager, que gerencia as operações sobre as tarefas, utilizando um dicionário (ou outra estrutura de dados) para armazenar e manipular as tarefas.
README.md	Documento explicativo que contém as instruções de uso, configuração do ambiente e descrição geral do projeto.




