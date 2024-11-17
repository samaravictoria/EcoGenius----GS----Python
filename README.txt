EcoGenius - Transformando Sustentabilidade em Soluções Digitais

## Sobre a EcoGenius
A EcoGenius é uma startup inovadora comprometida com o desenvolvimento sustentável 
e o impacto social positivo. Nosso objetivo é conectar ideias brilhantes e 
serviços ecológicos a pessoas e empresas que buscam transformar suas ações em 
soluções sustentáveis e economicamente viáveis.

### Missão
Criar uma plataforma digital robusta que facilite a gestão, 
compartilhamento e aplicação de ideias e serviços sustentáveis, 
permitindo que indivíduos e empresas contribuam para um futuro mais verde.

----

## A Ideia por Trás da EcoGenius
A EcoGenius centraliza o gerenciamento de ideias inovadoras e serviços sustentáveis, 
oferecendo uma interface intuitiva e poderosa para usuários interessados em fazer 
parte da revolução ecológica. A plataforma também permite:

- Cadastro de ideias relacionadas à sustentabilidade.
- Promoção de serviços ecológicos com impacto positivo.
- Conexão entre inovadores e empresas para execução de projetos verdes.

----

## Estrutura do Banco de Dados
O banco de dados da EcoGenius foi projetado para armazenar informações 
essenciais relacionadas aos usuários, ideias e serviços, 
garantindo integridade, eficiência e escalabilidade. A estrutura utiliza o 
Oracle Database e possui as seguintes tabelas principais:

### 1. Tabela `t_usuarios`
- Descrição: Gerencia os usuários cadastrados na plataforma.
- Campos:
  - `id_usuario`: ID único do usuário.
  - `nm_usuario`: Nome do usuário.
  - `ds_email`: E-mail do usuário.
  - `ds_senha`: Senha (criptografada) do usuário.
  - `dt_nascimento`: Data de nascimento.

### 2. Tabela `t_ideias`
- Descrição: Armazena ideias criadas pelos usuários.
- Campos:
  - `id_ideia`: ID único da ideia.
  - `nm_ideia`: Nome da ideia.
  - `ds_descricao`: Descrição detalhada da ideia.

### 3. Tabela `t_servicos`
- Descrição: Gerencia serviços ecológicos cadastrados na plataforma.
- Campos:
  - `id_servico`: ID único do serviço.
  - `nm_servico`: Nome do serviço.
  - `ds_descricao`: Descrição do serviço.
  - `tipo_servico`: Tipo do serviço.

### Relacionamentos
O banco foi projetado para ser modular e extensível, 
permitindo integrações futuras, como métricas de impacto e avaliações dos serviços.

----

## CRUD - Gerenciamento Completo
O sistema de CRUD foi desenvolvido para permitir o gerenciamento de 
todas as informações contidas no banco de dados, integrando de forma 
intuitiva o front-end e o banco Oracle.

### Funcionalidades do CRUD
- Usuários:
  - Inserir: Cadastro de novos usuários.
  - Consultar: Visualização detalhada dos usuários cadastrados.
  - Atualizar: Alteração de informações como nome e e-mail.
  - Excluir: Remoção de usuários inativos.

- Ideias:
  - Inserir: Criação de ideias relacionadas à sustentabilidade.
  - Consultar: Filtros por categoria, data e título.
  - Atualizar: Edição do conteúdo das ideias.
  - Excluir: Remoção de ideias obsoletas ou duplicadas.

- Serviços:
  - Inserir: Cadastro de serviços ecológicos, incluindo descrição e preço.
  - Consultar: Filtros por preço, categoria e data de criação.
  - Atualizar: Alteração de informações de serviços.
  - Excluir: Exclusão de serviços indisponíveis.

### Exportação de Dados
As consultas podem ser exportadas em formato JSON, 
facilitando o compartilhamento e análise das informações fora da plataforma.

---

## Tecnologias Utilizadas
- Linguagens: Python (CRUD), PL/SQL.
- Banco de Dados: Oracle Database.
- Validações e Segurança:
  - Validação de entradas.
  - Tratamento de exceções.
  - Criptografia para dados sensíveis.
- Formatos de Exportação: JSON

----------

Please see the cx_Oracle home page for links to documentation, source, build
and installation instructions:

https://oracle.github.io/python-cx_Oracle/index.html

