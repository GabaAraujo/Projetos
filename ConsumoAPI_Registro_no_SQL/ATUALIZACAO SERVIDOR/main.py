import requests
import pyodbc
from datetime import datetime, timedelta

def create_connection(driver, server, database, username, password):
    try:
        conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}")
        print("Conexão com o banco de dados SQL Server bem-sucedida")
        return conn
    except pyodbc.Error as e:
        print(e)
        return None

def get_most_recent_date(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX(data) FROM {table_name}")
    most_recent_date = cursor.fetchone()[0]
    if most_recent_date:
        return datetime.strptime(most_recent_date, "%Y-%m-%dT%H:%M:%S.%fZ")  # Parse the date string into a datetime object
    else:
        return datetime(2024, 5, 15)  # Default date if no data is found

def create_table(response, conn, table_name):
    try:
        response_data = response.json()
        fields = response_data[0].keys()
    except (IndexError, ValueError):
        print("Não há dados para criar a tabela para esta data.")
        return
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
    if cursor.fetchone()[0] == 0:
        columns = ', '.join([f'[{field}] VARCHAR(MAX)' for field in fields])
        create_table_query = f'CREATE TABLE {table_name} ({columns})'
        cursor.execute(create_table_query)
        conn.commit()
        print(f'Table {table_name} created successfully with columns: {", ".join(fields)}')
    else:
        print(f'Table {table_name} already exists.')

def insert_values(response, conn, table_name):
    response_data = response.json()
    try:
        fields = response_data[0].keys()
    except IndexError:
        print("Não há dados para inserir para esta data.")
        return
    
    cursor = conn.cursor()
    insert_query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['?' for _ in fields])})"
    for row in response_data:
        values = [str(row[key]) for key in fields]
        cursor.execute(insert_query, values)
    conn.commit()
    print(f'Data inserted into {table_name} successfully.')

def alter_table_column_size(conn, table_name, column_name, new_size='MAX'):
    cursor = conn.cursor()
    alter_query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} VARCHAR({new_size})"
    cursor.execute(alter_query)
    conn.commit()
    print(f"Column {column_name} in table {table_name} altered successfully to size {new_size}.")

# Configuration
url = "https://apiv3.vexsoft.com.br/vistoria/axn105"
params_fixed = {"limite": 50}

conn = create_connection(
    driver='SQL Server',     
    server='18.229.225.139',
    database='BMCLIENTES',
    username='api_vex',
    password='hexagon@vex'
)

if conn:
    table_name = 'BdVexSoft'
    data_inicial = get_most_recent_date(conn, table_name)
    data_final = data_inicial + timedelta(days=1)
    data_atual = datetime.now()

    while data_final < data_atual:
        params_fixed["data_inicial"] = data_inicial.strftime("%Y-%m-%d")
        params_fixed["data_final"] = data_final.strftime("%Y-%m-%d")

        response = requests.post(url, json=params_fixed)

        if response.status_code == 200:
            create_table(response, conn, table_name)
            insert_values(response, conn, table_name)
            alter_table_column_size(conn, table_name, 'fotos')
        else:
            print("Erro ao enviar requisição. Código de status:", response.status_code)
        
        data_inicial = data_final
        data_final += timedelta(days=1)

    conn.close()
