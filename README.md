## Descrição do Problema
O **Sistema de Gerenciamento de Tarefas** é uma aplicação distribuída que segue o modelo cliente/servidor, onde múltiplos clientes podem se conectar ao servidor para realizar operações relacionadas a tarefas como:
- Criação de tarefas.
- Leitura de tarefas.
- Atualização de tarefas.
- Exclusão de tarefas.

O servidor mantém um conjunto de tarefas e processa as requisições dos clientes, garantindo que cada cliente tenha suas próprias tarefas independentes. Toda comunicação entre o cliente e o servidor é feita através de sockets, utilizando um protocolo de aplicação específico.

### Funcionalidades principais
- **Criar Tarefas:** Permite que o usuário crie uma tarefa com nome e descrição.
- **Ler Tarefas:** Permite que o usuário leia uma tarefa específica ou todas as tarefas.
- **Atualizar Tarefas:** Permite que o usuário atualize o nome e a descrição de uma tarefa existente.
- **Excluir Tarefas:** Permite que o usuário exclua uma tarefa.

## Arquivos do Projeto

| Nome do Arquivo      | Descrição |
|----------------------|-----------|
| **server.py**         | Implementa o servidor que gerencia as tarefas e responde às requisições dos clientes. |
| **client.py**         | Implementa o cliente que se conecta ao servidor para enviar comandos e manipular tarefas. |
| **command_processor.py** | Responsável por processar os comandos digitados pelo usuário no cliente. |
| **gerenciador_tarefas.py** | Implementa a lógica de gerenciamento de tarefas, incluindo criação, leitura, atualização, e exclusão de tarefas. |
| **history_manager.py** | Gerencia o histórico de comandos executados pelo cliente. |
| **network_utils.py**  | Contém funções utilitárias para enviar comandos e receber respostas via socket. |
| **estruturas/dicionario.py** | Implementa a estrutura de dados de tabela hash usada para armazenar as tarefas. |
| **estruturas/ListaEncadeada.py** | Implementa a lista encadeada para o histórico de comandos. |

## Pré-requisitos para Execução
Para rodar o projeto, você precisará dos seguintes pacotes e bibliotecas:

- **Python 3.x**: Certifique-se de ter o Python instalado.
- **Numpy**: Para instalar, execute o seguinte comando:

  ```bash
  pip install numpy
Como instalar os pacotes:
Clone o repositório.
Navegue até o diretório do projeto.
Instale as dependências usando o comando pip install numpy se necessário.
Protocolo da Aplicação
O protocolo de comunicação entre cliente e servidor utiliza comandos de texto separados por barras verticais |. Cada comando enviado pelo cliente ao servidor deve estar no seguinte formato:

criar|<nome_da_tarefa>|<descrição>: Cria uma nova tarefa com o nome e a descrição fornecidos.
ler|<id_tarefa>: Lê uma tarefa específica, identificada pelo ID.
ler: Lê todas as tarefas existentes.
atualizar|<id_tarefa>|<novo_nome>|<nova_descrição>: Atualiza o nome e a descrição de uma tarefa.
deletar|<id_tarefa>: Exclui uma tarefa com o ID fornecido.
historico: Retorna o histórico de comandos executados no cliente.
Códigos de Status
Abaixo está a lista dos códigos de status utilizados no protocolo, juntamente com suas mensagens e descrições:

Código	Mensagem	Descrição

200	Operação realizada com sucesso.	A operação foi concluída com êxito.

201	Tarefa criada com sucesso.	A tarefa foi criada corretamente no servidor.

202	Tarefa atualizada com sucesso.	A tarefa foi atualizada com os novos dados fornecidos.

203	Tarefa lida com sucesso.	A tarefa foi lida com sucesso pelo servidor.

204	Tarefa excluída com sucesso.	A tarefa foi excluída corretamente do sistema.

205	Nenhuma tarefa foi criada ainda.	Não há tarefas criadas no momento. O usuário deve criar uma nova tarefa.

300	Tarefa não encontrada.	A tarefa solicitada não foi encontrada no sistema.

400	Erro na requisição.	A requisição enviada está incompleta ou possui parâmetros inválidos.

404	Tarefa não existe.	A tarefa solicitada não existe.

500	Erro interno do servidor.	Ocorreu um erro interno no servidor ao processar a requisição.

Instruções para Execução
Como iniciar o servidor:
Navegue até o diretório do projeto.

Execute o servidor com o seguinte comando no terminal:

bash
Copiar código
python server.py
O servidor iniciará e ficará em escuta aguardando conexões de clientes.

Como iniciar o cliente:
Em outro terminal, execute o cliente com o comando:

bash
Copiar código
python client.py
O cliente conectará ao servidor, e você poderá interagir usando os comandos disponíveis.

Fluxo de utilização:
Após iniciar o cliente, uma lista de comandos será exibida. Você pode utilizar os seguintes comandos:

criar: Para criar uma nova tarefa.
ler: Para ler uma tarefa específica ou todas as tarefas.
atualizar: Para atualizar uma tarefa existente.
deletar: Para excluir uma tarefa.
historico: Para exibir o histórico de comandos executados.
O servidor irá processar suas requisições e retornar as respostas apropriadas com códigos de status e mensagens, conforme especificado na tabela de códigos de status.