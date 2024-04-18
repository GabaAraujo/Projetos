import requests
import pyodbc
from datetime import datetime, timedelta

# Função para criar uma conexão com o banco de dados SQL Server
def create_connection(driver, server, database, username, password):
    conn = None
    try:
        conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}")
        print("Conexão com o banco de dados SQL Server bem-sucedida")
    except pyodbc.Error as e:
        print(e)
    return conn

def cria_tabela(response, conn, nome_tabela):
    try:
        response_data = response.json()  # Converte o conteúdo da resposta para um objeto Python
        campos = response_data[0].keys() # Pega apenas as chaves de um registro do banco
    except IndexError:
        print("Não há dados para criar a tabela para esta data.")
        return
    
    table_name = nome_tabela # Atribui o valor da tabela
    cursor = conn.cursor() # Libera o terminal do SQL com a conexão, e atribui a variavel

    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'") # Verifica a tabela se ela existe
    if cursor.fetchone()[0] == 0: #se não existir ==0 /se existir == 1
        # Registra os valores do campo /tamanho de 5000 para o maior campo
        columns = ','.join([f'[{campo}] VARCHAR(8000)' for campo in campos]) # Faz uma query com cada valor do campo, sendo um array pegando todos os dados do campo repitindo o tamanho 
        create_table_query = f'CREATE TABLE {table_name} ({columns})' # Cria a tabela com as colunas
        cursor.execute(create_table_query) #executa chamando o cursor->(cursor seria o terminal do sql server)
        conn.commit() #comita -> faz a execução
        print(f'Table {table_name} created successfully with columns: {", ".join(campos)}')
    else:
         print(f'Table {table_name} already exists.')

def alter_table_column_size(conn, table_name, column_name, new_size):
    cursor = conn.cursor()
    alter_query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} VARCHAR({new_size})"
    cursor.execute(alter_query)
    conn.commit()
    print(f"Column {column_name} in table {table_name} altered successfully with size {new_size}.")

def insere_valores(response, conn, table_name):
    response_data = response.json()  # Converte o conteúdo da resposta para um objeto Python
    try:
        campos = response_data[0].keys() # Pega apenas as chaves de um registro do banco
    except IndexError:
        print("Não há dados para inserir para esta data.")
        return
    
    cursor = conn.cursor()
    insert_query = f"INSERT INTO {table_name} ({', '.join(campos)}) VALUES ({', '.join(['?' for _ in campos])})"
    for row in response_data:
        values = [str(row[key]) for key in campos]  # Convert all values to string
        cursor.execute(insert_query, values) #Para cada registro, cria uma lista de valores, onde cada valor é obtido da linha atual (row) e da coluna correspondente (representada por key), convertendo-os para string.
    conn.commit()
    print(f'Data inserted into {table_name} successfully.')

# URL da API
url = "https://apiv3.vexsoft.com.br/vistoria/axn105"

# Parâmetros fixos da requisição
params_fixos = {
    "limite": 100
}

# Conectar-se ao banco de dados SQL Server e atribui a variavel
conn = create_connection(
    driver='SQL Server',     
    server='GEO-WNB24020193',
    database='Teste',
    username='',
    password=''
)

# Calcula as datas d-1 e d-2
data_atual = datetime.now()
data_inicial = datetime(2023, 3, 1)  # Defina a data inicial aqui
data_final = data_inicial + timedelta(days=1)

while data_final < data_atual:
    # Atualiza os parâmetros da requisição
    params_fixos["data_inicial"] = data_inicial.strftime("%Y-%m-%d")
    params_fixos["data_final"] = data_final.strftime("%Y-%m-%d")

    response = requests.post(url, json=params_fixos)

    if response.status_code == 200:
        cria_tabela(response, conn, nome_tabela='TabelaVex') #envia a requisicao, a conexao, #nome da tabela
        insere_valores(response, conn, table_name='TabelaVex')
        alter_table_column_size(conn, 'TabelaVex', 'fotos', 'MAX')
    else:
        # Se não for bem-sucedida, exibir o código de status
        print("Erro ao enviar requisição. Código de status:", response.status_code)
    
    # Atualiza as datas para a próxima iteração
    data_inicial = data_final
    data_final += timedelta(days=1)

conn.close()
