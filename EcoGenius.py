import cx_Oracle
import json
from datetime import datetime

# Configurações do banco de dados
DB_USER = 'rm558043'
DB_PASSWORD = 'fiap24'
host = 'oracle.fiap.com.br'
porta = '1521'
SID = 'orcl'

# Inicializa o cliente Oracle
try:
    cx_Oracle.init_oracle_client(lib_dir=r"C:/Program Files/instantclient_23_5 (1)/instantclient_23_5")
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
        print("\n--- Menu Principal ---")
        print("1. Gerenciar Usuários")
        print("2. Gerenciar Ideias")
        print("3. Gerenciar Serviços")
        print("4. Exportar Dados")
        print("5. Sair")
        print("----------------------")
        
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
        print("\n--- Gerenciar Usuários ---")
        print("1. Inserir Usuário")
        print("2. Atualizar Usuário")
        print("3. Excluir Usuário")
        print("4. Consultar Usuários")
        print("5. Voltar")
        print("--------------------------")
        
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
            return
        else:
            print("Opção inválida. Tente novamente.")

def insert_user():
    nome = input("Digite o nome do usuário: ").strip()
    email = input("Digite o email: ").strip()
    senha = input("Digite a senha: ").strip()
    dt_nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()

    if validate_date(dt_nascimento):
        query = """INSERT INTO t_usuario (id_usuario, nm_usuario, ds_email, ds_senha, dt_nascimento)
                   VALUES (seq_usuario.NEXTVAL, :nome, :email, :senha, TO_DATE(:dt_nascimento, 'YYYY-MM-DD'))"""
        execute_query(query, {'nome': nome, 'email': email, 'senha': senha, 'dt_nascimento': dt_nascimento})
        print("Usuário inserido com sucesso!")

def update_user():
    id_usuario = input("Digite o ID do usuário a ser atualizado: ").strip()
    nome = input("Digite o novo nome: ").strip()
    email = input("Digite o novo email: ").strip()
    senha = input("Digite a nova senha: ").strip()
    dt_nascimento = input("Digite a nova data de nascimento (YYYY-MM-DD): ").strip()

    if validate_date(dt_nascimento):
        query = """UPDATE t_usuario
                   SET nm_usuario = :nome, ds_email = :email, ds_senha = :senha, 
                       dt_nascimento = TO_DATE(:dt_nascimento, 'YYYY-MM-DD')
                   WHERE id_usuario = :id_usuario"""
        execute_query(query, {'nome': nome, 'email': email, 'senha': senha, 'dt_nascimento': dt_nascimento, 'id_usuario': id_usuario})
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
            print(f"ID: {row[0]}, Nome: {row[1]}, Email: {row[2]}, Data de Nascimento: {row[3]}")
    else:
        print("Nenhum usuário encontrado.")
        
# Gerenciamento de Ideias
def ideas_menu():
    while True:
        print("\n--- Gerenciar Ideias ---")
        print("1. Inserir Ideia")
        print("2. Atualizar Ideia")
        print("3. Excluir Ideia")
        print("4. Consultar Ideias")
        print("5. Voltar")
        print("------------------------")
        
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
            return
        else:
            print("Opção inválida. Tente novamente.")

def insert_idea():
    id_usuario = input("Digite o ID do usuário: ").strip()
    nm_ideia = input("Digite o nome da ideia: ").strip()
    ds_descricao = input("Digite a descrição da ideia: ").strip()

    query = """INSERT INTO t_ideias (id_ideia, id_usuario, nm_ideia, ds_descricao)
               VALUES (seq_ideias.NEXTVAL, :id_usuario, :nm_ideia, :ds_descricao)"""
    execute_query(query, {'id_usuario': id_usuario, 'nm_ideia': nm_ideia, 'ds_descricao': ds_descricao})
    print("Ideia inserida com sucesso!")

def update_idea():
    id_ideia = input("Digite o ID da ideia a ser atualizada: ").strip()
    nm_ideia = input("Digite o novo nome: ").strip()
    ds_descricao = input("Digite a nova descrição: ").strip()

    query = """UPDATE t_ideias
               SET nm_ideia = :nm_ideia, ds_descricao = :ds_descricao
               WHERE id_ideia = :id_ideia"""
    execute_query(query, {'nm_ideia': nm_ideia, 'ds_descricao': ds_descricao, 'id_ideia': id_ideia})
    print("Ideia atualizada com sucesso!")

def delete_idea():
    id_ideia = input("Digite o ID da ideia a ser excluída: ").strip()
    query = "DELETE FROM t_ideias WHERE id_ideia = :id_ideia"
    execute_query(query, {'id_ideia': id_ideia})
    print("Ideia excluída com sucesso!")

def query_ideas():
    query = "SELECT id_ideia, id_usuario, nm_ideia, ds_descricao FROM t_ideias ORDER BY id_ideia"
    results = execute_query(query, fetch=True)
    if results:
        for row in results:
            print(f"ID: {row[0]}, ID Usuário: {row[1]}, Nome: {row[2]}, Descrição: {row[3]}")
    else:
        print("Nenhuma ideia encontrada.")

# Gerenciamento de Serviços
def services_menu():
    while True:
        print("\n--- Gerenciar Serviços ---")
        print("1. Inserir Serviço")
        print("2. Atualizar Serviço")
        print("3. Excluir Serviço")
        print("4. Consultar Serviços")
        print("5. Voltar")
        print("-------------------------")
        
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
            return
        else:
            print("Opção inválida. Tente novamente.")

def insert_service():
    id_usuario = input("Digite o ID do usuário: ").strip()
    nm_servico = input("Digite o nome do serviço: ").strip()
    ds_descricao = input("Digite a descrição do serviço: ").strip()

    query = """INSERT INTO t_servicos (id_servico, id_usuario, nm_servico, ds_descricao)
               VALUES (seq_servicos.NEXTVAL, :id_usuario, :nm_servico, :ds_descricao)"""
    execute_query(query, {'id_usuario': id_usuario, 'nm_servico': nm_servico, 'ds_descricao': ds_descricao})
    print("Serviço inserido com sucesso!")

def update_service():
    id_servico = input("Digite o ID do serviço a ser atualizado: ").strip()
    nm_servico = input("Digite o novo nome do serviço: ").strip()
    ds_descricao = input("Digite a nova descrição: ").strip()

    query = """UPDATE t_servicos
               SET nm_servico = :nm_servico, ds_descricao = :ds_descricao
               WHERE id_servico = :id_servico"""
    execute_query(query, {'nm_servico': nm_servico, 'ds_descricao': ds_descricao, 'id_servico': id_servico})
    print("Serviço atualizado com sucesso!")

def delete_service():
    id_servico = input("Digite o ID do serviço a ser excluído: ").strip()
    query = "DELETE FROM t_servicos WHERE id_servico = :id_servico"
    execute_query(query, {'id_servico': id_servico})
    print("Serviço excluído com sucesso!")

def query_services():
    query = "SELECT id_servico, id_usuario, nm_servico, ds_descricao FROM t_servicos ORDER BY id_servico"
    results = execute_query(query, fetch=True)
    if results:
        for row in results:
            print(f"ID: {row[0]}, ID Usuário: {row[1]}, Nome: {row[2]}, Descrição: {row[3]}")
    else:
        print("Nenhum serviço encontrado.")

    # Validando o tipo de serviço
    while True:
        tipo_servico = input("Digite o tipo do serviço (Consulta, Dicas, Informação ou Energia): ").strip().upper()
        if tipo_servico in ['CONSULTA', 'DICAS', 'INFORMACAO', 'ENERGIA']:
            break
        else:
            print("Tipo de serviço inválido. Por favor, escolha entre Consulta, Dicas, Informação ou Energia.")

    query = """INSERT INTO t_servicos (id_servico, id_usuario, nm_servico, ds_servico, tipo_servico)
               VALUES (seq_servicos.NEXTVAL, :id_usuario, :nm_servico, :ds_servico, :tipo_servico)"""
    execute_query(query, {'id_usuario': id_usuario, 'nm_servico': nm_servico, 'ds_servico': ds_servico, 'tipo_servico': tipo_servico})
    print("Serviço inserido com sucesso!")

    # Validando o tipo de serviço
    while True:
        tipo_servico = input("Digite o novo tipo do serviço (Consulta, Dicas, Informação ou Energia): ").strip().upper()
        if tipo_servico in ['CONSULTA', 'DICAS', 'INFORMACAO', 'ENERGIA']:
            break
        else:
            print("Tipo de serviço inválido. Por favor, escolha entre CConsulta, Dicas, Informação ou Energia.")

    query = """UPDATE t_servicos
               SET nm_servico = :nm_servico, ds_servico = :ds_servico, tipo_servico = :tipo_servico
               WHERE id_servico = :id_servico"""
    execute_query(query, {'nm_servico': nm_servico, 'ds_servico': ds_servico, 'tipo_servico': tipo_servico, 'id_servico': id_servico})
    print("Serviço atualizado com sucesso!")

def delete_service():
    id_servico = input("Digite o ID do serviço a ser excluído: ").strip()
    query = "DELETE FROM t_servicos WHERE id_servico = :id_servico"
    execute_query(query, {'id_servico': id_servico})
    print("Serviço excluído com sucesso!")

def query_services():
    query = "SELECT id_servico, id_usuario, nm_servico, ds_servico, tipo_servico FROM t_servicos ORDER BY id_servico"
    results = execute_query(query, fetch=True)
    if results:
        for row in results:
            print(f"ID: {row[0]}, ID Usuário: {row[1]}, Nome: {row[2]}, Descrição: {row[3]}, Tipo: {row[4]}")
    else:
        print("Nenhum serviço encontrado.")

# Consulta 1: Filtrar usuários por nome
def query_users_by_name():
    """
    Consulta 1: Filtrar usuários por nome.
    """
    try:
        nome = input("Digite o nome do usuário para filtrar: ").strip()
        query = "SELECT * FROM t_usuario WHERE UPPER(nm_usuario) LIKE UPPER(:nome)"
        
        # Executa a consulta com o parâmetro nome
        results = execute_query(query, {'nome': f'%{nome}%'}, fetch=True)
        
        if results:
            # Cria uma conexão para pegar as colunas (se necessário)
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, {'nome': f'%{nome}%'})
            colunas = [desc[0] for desc in cursor.description]  # Pegando os nomes das colunas
            
            # Criando um dicionário com os dados
            dados = [dict(zip(colunas, linha)) for linha in results]
            
            print(f"\nUsuários encontrados com o nome '{nome}':")
            for usuario in dados:
                print(f"ID: {usuario['ID_USUARIO']}, Nome: {usuario['NM_USUARIO']}, Email: {usuario['DS_EMAIL']}, Data de Nascimento: {usuario['DT_NASCIMENTO']}")
        else:
            print("Nenhum usuário encontrado com esse nome.")
    except Exception as e:
        print(f"Erro ao consultar os usuários: {e}")

# Consulta 2: Filtrar ideias por nome
def query_ideas_by_name():
    """
    Consulta 2: Filtrar ideias por nome.
    """
    try:
        nome_ideia = input("Digite o nome da ideia para filtrar: ").strip()
        query = "SELECT * FROM t_ideias WHERE UPPER(nm_ideia) LIKE UPPER(:nome_ideia)"
        
        # Executa a consulta com o parâmetro nome_ideia
        results = execute_query(query, {'nome_ideia': f'%{nome_ideia}%'}, fetch=True)
        
        if results:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, {'nome_ideia': f'%{nome_ideia}%'})
            colunas = [desc[0] for desc in cursor.description]  # Pegando os nomes das colunas
            
            dados = [dict(zip(colunas, linha)) for linha in results]  # Criando um dicionário com os dados
            print(f"\nIdeias encontradas com o nome '{nome_ideia}':")
            for dado in dados:
                print(dado)
        else:
            print("Nenhuma ideia encontrada com esse nome.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Consulta 3: Filtrar ideias por descrição
def query_ideas_by_description():
    """
    Consulta 3: Filtrar ideias por descrição.
    """
    try:
        descricao = input("Digite a descrição da ideia para filtrar: ").strip()
        query = "SELECT * FROM t_ideias WHERE UPPER(ds_descricao) LIKE UPPER(:descricao)"
        
        # Executa a consulta com o parâmetro descrição
        results = execute_query(query, {'descricao': f'%{descricao}%'}, fetch=True)
        
        if results:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(query, {'descricao': f'%{descricao}%'})
            colunas = [desc[0] for desc in cursor.description]  # Pegando os nomes das colunas
            
            dados = [dict(zip(colunas, linha)) for linha in results]  # Criando um dicionário com os dados
            print(f"\nIdeias encontradas com a descrição '{descricao}':")
            for dado in dados:
                print(dado)
        else:
            print("Nenhuma ideia encontrada com essa descrição.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Exportação de dados para JSON
def export_data_menu():
    while True:
        print("\n--- Exportar Dados ---")
        print("1. Exportar Usuários")
        print("2. Exportar Ideias")
        print("3. Exportar Serviços")
        print("4. Voltar")
        print("-----------------------")
        
        choice = input("Escolha uma opção: ").strip()
        if choice == '1':
            export_users()
        elif choice == '2':
            export_ideas()
        elif choice == '3':
            export_services()
        elif choice == '4':
            return
        else:
            print("Opção inválida. Tente novamente.")

def export_users():
    query = "SELECT id_usuario, nm_usuario, ds_email, dt_nascimento FROM t_usuario"
    results = execute_query(query, fetch=True)
    if results:
        with open('users.json', 'w') as f:
            json.dump(results, f, default=str)
        print("Usuários exportados para 'users.json'")
    else:
        print("Nenhum dado de usuário encontrado para exportação.")

def export_ideas():
    query = "SELECT id_ideia, id_usuario, nm_ideia, ds_descricao FROM t_ideias"
    results = execute_query(query, fetch=True)
    if results:
        with open('ideas.json', 'w') as f:
            json.dump(results, f, default=str)
        print("Ideias exportadas para 'ideas.json'")
    else:
        print("Nenhum dado de ideia encontrado para exportação.")

def export_services():
    query = "SELECT id_servico, id_usuario, nm_servico, ds_descricao FROM t_servicos"
    results = execute_query(query, fetch=True)
    if results:
        with open('services.json', 'w') as f:
            json.dump(results, f, default=str)
        print("Serviços exportados para 'services.json'")
    else:
        print("Nenhum dado de serviço encontrado para exportação.")

# Inicialização do sistema
if __name__ == "__main__":
    print("Bem-vindo ao Sistema CRUD!")
    main_menu()
