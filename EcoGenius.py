import cx_Oracle
import json
from datetime import datetime
import cx_Oracle

# Configurações do banco de dados
DB_USER = 'rm558043'
DB_PASSWORD = 'fiap24'
host = 'oracle.fiap.com.br'
porta = '1521'
SID = 'orcl'

# Inicializa o cliente Oracle
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient-basic-windows.x64-23.5.0.24.07\instantclient_23_5")
except Exception as e:
    print("Erro na inicialização do 'client': ", e)
else:
    print('Cliente Oracle inicializado com sucesso!!!')

# Função para conectar ao banco de dados
def get_connection():
    try:
        # Cria a string DSN para conectar
        dsn_string = cx_Oracle.makedsn(host, porta, SID)
        
        # Estabelece a conexão
        connection = cx_Oracle.connect(
            user=DB_USER, 
            password=DB_PASSWORD, 
            dsn=dsn_string, 
            encoding="UTF-8"
        )
        return connection
    except cx_Oracle.DatabaseError as e:
        print("Erro ao conectar ao banco de dados:", e)
        exit()

# Função para exibir o menu principal
def main_menu():
    while True:
        print("\n======== MENU PRINCIPAL ========")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Ideias")
        print("3. Gerenciar Serviços")
        print("4. Exportar Dados")
        print("5. Sair")
        print("================================")

        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            user_menu()
        elif choice == '2':
            ideas_menu()
        elif choice == '3':
            services_menu()
        elif choice == '4':
            export_data_menu()
        elif choice == '5':
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Utilitário para validar datas
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Data inválida! Use o formato YYYY-MM-DD.")
        return None

# Função CRUD genérica
def execute_query(query, params=None, fetch=False):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or {})
                if fetch:
                    return cursor.fetchall()
                conn.commit()
    except cx_Oracle.DatabaseError as e:
        print("Erro ao executar a operação no banco de dados:", e)

# Gerenciamento de Usuários
def user_menu():
    while True:
        print("\n--- Gerenciamento de Usuários ---")
        print("1. Inserir Usuário")
        print("2. Atualizar Usuário")
        print("3. Excluir Usuário")
        print("4. Consultar Usuários")
        print("5. Voltar")
        print("---------------------------------")

        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            insert_user()
        elif choice == '2':
            update_user()
        elif choice == '3':
            delete_user()
        elif choice == '4':
            query_users()
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def insert_user():
    nome = input("Digite o nome do usuário: ").strip()
    email = input("Digite o e-mail: ").strip()
    senha = input("Digite a senha: ").strip()
    nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()

    if validate_date(nascimento):
        query = """INSERT INTO t_usuario (id_usuario, nm_usuario, ds_email, ds_senha, dt_nascimento)
                   VALUES (seq_usuario.NEXTVAL, :nome, :email, :senha, TO_DATE(:nascimento, 'YYYY-MM-DD'))"""
        execute_query(query, {'nome': nome, 'email': email, 'senha': senha, 'nascimento': nascimento})
        print("Usuário inserido com sucesso!")

def update_user():
    id_usuario = input("Digite o ID do usuário a ser atualizado: ").strip()
    nome = input("Digite o novo nome: ").strip()
    email = input("Digite o novo e-mail: ").strip()
    senha = input("Digite a nova senha: ").strip()
    nascimento = input("Digite a nova data de nascimento (YYYY-MM-DD): ").strip()

    if validate_date(nascimento):
        query = """UPDATE t_usuario
                   SET nm_usuario = :nome, ds_email = :email, ds_senha = :senha, 
                       dt_nascimento = TO_DATE(:nascimento, 'YYYY-MM-DD')
                   WHERE id_usuario = :id_usuario"""
        execute_query(query, {'nome': nome, 'email': email, 'senha': senha, 'nascimento': nascimento, 'id_usuario': id_usuario})
        print("Usuário atualizado com sucesso!")

def delete_user():
    id_usuario = input("Digite o ID do usuário a ser excluído: ").strip()
    query = "DELETE FROM t_usuario WHERE id_usuario = :id_usuario"
    execute_query(query, {'id_usuario': id_usuario})
    print("Usuário excluído com sucesso!")

def query_users():
    query = "SELECT id_usuario, nm_usuario, ds_email, dt_nascimento FROM t_usuario ORDER BY id_usuario"
    results = execute_query(query, fetch=True)
    if results:
        for row in results:
            print(f"ID: {row[0]}, Nome: {row[1]}, E-mail: {row[2]}, Nascimento: {row[3]}")
    else:
        print("Nenhum usuário encontrado.")
        
# Gerenciamento de Ideias
def ideas_menu():
    while True:
        print("\n--- Gerenciamento de Ideias ---")
        print("1. Inserir Ideia")
        print("2. Atualizar Ideia")
        print("3. Excluir Ideia")
        print("4. Consultar Ideias")
        print("5. Voltar")
        print("-------------------------------")

        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            insert_idea()
        elif choice == '2':
            update_idea()
        elif choice == '3':
            delete_idea()
        elif choice == '4':
            query_ideas()
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def insert_idea():
    titulo = input("Digite o título da ideia: ").strip()
    descricao = input("Digite a descrição da ideia: ").strip()
    categoria = input("Digite a categoria da ideia: ").strip()
    data_criacao = input("Digite a data de criação (YYYY-MM-DD): ").strip()

    if validate_date(data_criacao):
        query = """INSERT INTO t_ideias (id_ideia, ds_titulo, ds_descricao, ds_categoria, dt_criacao)
                   VALUES (seq_ideia.NEXTVAL, :titulo, :descricao, :categoria, TO_DATE(:data_criacao, 'YYYY-MM-DD'))"""
        execute_query(query, {'titulo': titulo, 'descricao': descricao, 'categoria': categoria, 'data_criacao': data_criacao})
        print("Ideia inserida com sucesso!")

def update_idea():
    id_ideia = input("Digite o ID da ideia a ser atualizada: ").strip()
    titulo = input("Digite o novo título: ").strip()
    descricao = input("Digite a nova descrição: ").strip()
    categoria = input("Digite a nova categoria: ").strip()
    data_criacao = input("Digite a nova data de criação (YYYY-MM-DD): ").strip()

    if validate_date(data_criacao):
        query = """UPDATE t_ideias
                   SET ds_titulo = :titulo, ds_descricao = :descricao, ds_categoria = :categoria,
                       dt_criacao = TO_DATE(:data_criacao, 'YYYY-MM-DD')
                   WHERE id_ideia = :id_ideia"""
        execute_query(query, {'titulo': titulo, 'descricao': descricao, 'categoria': categoria, 'data_criacao': data_criacao, 'id_ideia': id_ideia})
        print("Ideia atualizada com sucesso!")

def delete_idea():
    id_ideia = input("Digite o ID da ideia a ser excluída: ").strip()
    query = "DELETE FROM t_ideias WHERE id_ideia = :id_ideia"
    execute_query(query, {'id_ideia': id_ideia})
    print("Ideia excluída com sucesso!")

def query_ideas():
    query = "SELECT id_ideia, ds_titulo, ds_descricao, ds_categoria, dt_criacao FROM t_ideias ORDER BY id_ideia"
    results = execute_query(query, fetch=True)
    if results:
        for row in results:
            print(f"ID: {row[0]}, Título: {row[1]}, Descrição: {row[2]}, Categoria: {row[3]}, Data de Criação: {row[4]}")
    else:
        print("Nenhuma ideia encontrada.")

# Gerenciamento de Serviços
def services_menu():
    while True:
        print("\n--- Gerenciamento de Serviços ---")
        print("1. Inserir Serviço")
        print("2. Atualizar Serviço")
        print("3. Excluir Serviço")
        print("4. Consultar Serviços")
        print("5. Voltar")
        print("---------------------------------")

        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            insert_service()
        elif choice == '2':
            update_service()
        elif choice == '3':
            delete_service()
        elif choice == '4':
            query_services()
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

def insert_service():
    nome = input("Digite o nome do serviço: ").strip()
    descricao = input("Digite a descrição do serviço: ").strip()
    preco = input("Digite o preço do serviço: ").strip()
    data_criacao = input("Digite a data de criação (YYYY-MM-DD): ").strip()

    if validate_date(data_criacao):
        query = """INSERT INTO t_servicos (id_servico, nm_servico, ds_descricao, vl_preco, dt_criacao)
                   VALUES (seq_servico.NEXTVAL, :nome, :descricao, :preco, TO_DATE(:data_criacao, 'YYYY-MM-DD'))"""
        execute_query(query, {'nome': nome, 'descricao': descricao, 'preco': preco, 'data_criacao': data_criacao})
        print("Serviço inserido com sucesso!")

def update_service():
    id_servico = input("Digite o ID do serviço a ser atualizado: ").strip()
    nome = input("Digite o novo nome do serviço: ").strip()
    descricao = input("Digite a nova descrição: ").strip()
    preco = input("Digite o novo preço: ").strip()
    data_criacao = input("Digite a nova data de criação (YYYY-MM-DD): ").strip()

    if validate_date(data_criacao):
        query = """UPDATE t_servicos
                   SET nm_servico = :nome, ds_descricao = :descricao, vl_preco = :preco,
                       dt_criacao = TO_DATE(:data_criacao, 'YYYY-MM-DD')
                   WHERE id_servico = :id_servico"""
        execute_query(query, {'nome': nome, 'descricao': descricao, 'preco': preco, 'data_criacao': data_criacao, 'id_servico': id_servico})
        print("Serviço atualizado com sucesso!")

def delete_service():
    id_servico = input("Digite o ID do serviço a ser excluído: ").strip()
    query = "DELETE FROM t_servicos WHERE id_servico = :id_servico"
    execute_query(query, {'id_servico': id_servico})
    print("Serviço excluído com sucesso!")

def query_services():
    query = "SELECT id_servico, nm_servico, ds_descricao, vl_preco, dt_criacao FROM t_servicos ORDER BY id_servico"
    results = execute_query(query, fetch=True)
    if results:
        for row in results:
            print(f"ID: {row[0]}, Nome: {row[1]}, Descrição: {row[2]}, Preço: {row[3]}, Data de Criação: {row[4]}")
    else:
        print("Nenhum serviço encontrado.")

# Consulta 1: Filtrar usuários por nome
def query_users_by_name():
    """
    Consulta os usuários no banco de dados filtrando pelo nome.
    """
    nome = input("Digite o nome do usuário para filtrar: ").strip()
    query = "SELECT * FROM t_usuario WHERE UPPER(nm_usuario) LIKE UPPER(:nome)"
    
    # Executa a consulta com o parâmetro nome
    results = execute_query(query, {'nome': f'%{nome}%'}, fetch=True)
    
    if results:
        colunas = [desc[0] for desc in get_connection().cursor().description]  # Pegando os nomes das colunas
        dados = [dict(zip(colunas, linha)) for linha in results]  # Criando um dicionário com os dados
        print(f"\nUsuários encontrados com o nome '{nome}':")
        for dado in dados:
            print(dado)
    else:
        print("Nenhum usuário encontrado com esse nome.")

# Consulta 2: Filtrar ideias por categoria e data de criação
def query_ideas_by_category_and_date():
    """
    Consulta as ideias no banco de dados filtrando por categoria e data de criação.
    """
    categoria = input("Digite a categoria das ideias para filtrar: ").strip()
    data_criacao = input("Digite a data de criação das ideias (YYYY-MM-DD): ").strip()
    
    if validate_date(data_criacao):
        query = """SELECT * FROM t_ideias WHERE UPPER(ds_categoria) = UPPER(:categoria) 
                   AND dt_criacao >= TO_DATE(:data_criacao, 'YYYY-MM-DD')"""
        
        # Executa a consulta com os parâmetros categoria e data de criação
        results = execute_query(query, {'categoria': categoria, 'data_criacao': data_criacao}, fetch=True)
        
        if results:
            colunas = [desc[0] for desc in get_connection().cursor().description]
            dados = [dict(zip(colunas, linha)) for linha in results]
            print(f"\nIdeias encontradas na categoria '{categoria}' a partir de {data_criacao}:")
            for dado in dados:
                print(dado)
        else:
            print("Nenhuma ideia encontrada com os filtros informados.")

# Consulta 3: Filtrar serviços por status e data de criação
def query_services_by_status_and_date():
    """
    Consulta os serviços no banco de dados filtrando por status e data de criação.
    """
    status = input("Digite o status do serviço para filtrar (ex: 'Em andamento'): ").strip()
    data_criacao = input("Digite a data de criação do serviço (YYYY-MM-DD): ").strip()

    if validate_date(data_criacao):
        query = """SELECT * FROM t_servicos WHERE UPPER(ds_status) = UPPER(:status) 
                   AND dt_criacao >= TO_DATE(:data_criacao, 'YYYY-MM-DD')"""
        
        # Executa a consulta com os parâmetros status e data de criação
        results = execute_query(query, {'status': status, 'data_criacao': data_criacao}, fetch=True)
        
        if results:
            colunas = [desc[0] for desc in get_connection().cursor().description]
            dados = [dict(zip(colunas, linha)) for linha in results]
            print(f"\nServiços encontrados com o status '{status}' a partir de {data_criacao}:")
            for dado in dados:
                print(dado)
        else:
            print("Nenhum serviço encontrado com os filtros informados.")

# Exportação de dados para JSON
def export_data_menu():
    tabela = input("Digite o nome da tabela para exportar (t_usuario, t_ideias, t_servicos): ").strip()
    query = f"SELECT * FROM {tabela}"
    results = execute_query(query, fetch=True)
    if results:
        colunas = [desc[0] for desc in get_connection().cursor().description]
        dados = [dict(zip(colunas, linha)) for linha in results]

        with open(f"{tabela}.json", "w", encoding="utf-8") as json_file:
            json.dump(dados, json_file, ensure_ascii=False, indent=4)
        print(f"Dados exportados para {tabela}.json com sucesso!")
    else:
        print(f"Nenhum dado encontrado na tabela {tabela}.")

# Inicialização do sistema
if __name__ == "__main__":
    print("Bem-vindo ao Sistema CRUD!")
    main_menu()
