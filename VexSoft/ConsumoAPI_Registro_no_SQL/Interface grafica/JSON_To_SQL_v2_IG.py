import requests
import pyodbc
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

def create_connection(driver, server, database, username, password):
    conn = None
    try:
        conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}")
        messagebox.showinfo("Sucesso", "Conexão com o banco de dados SQL Server bem-sucedida")
    except pyodbc.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
    return conn

def cria_tabela(response, conn, nome_tabela):
    response_data = response.json()
    campos = response_data[0].keys()
    
    table_name = nome_tabela
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
    if cursor.fetchone()[0] == 0:
        columns = ','.join([f'[{campo}] VARCHAR(8000)' for campo in campos])
        create_table_query = f'CREATE TABLE {table_name} ({columns})'
        cursor.execute(create_table_query)
        conn.commit()
        messagebox.showinfo("Sucesso", f'Tabela {table_name} criada com sucesso com colunas: {", ".join(campos)}')
    else:
        messagebox.showinfo("Info", f'Tabela {table_name} já existe.')

def alter_table_column_size(conn, table_name, column_name, new_size):
    cursor = conn.cursor()
    alter_query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} VARCHAR({new_size})"
    cursor.execute(alter_query)
    conn.commit()
    messagebox.showinfo("Sucesso", f'Coluna {column_name} na tabela {table_name} alterada com sucesso para o tamanho {new_size}.')

def insere_valores(response, conn, table_name):
    response_data = response.json()
    campos = response_data[0].keys()
    
    cursor = conn.cursor()
    insert_query = f"INSERT INTO {table_name} ({', '.join(campos)}) VALUES ({', '.join(['?' for _ in campos])})"
    for row in response_data:
        values = [str(row[key]) for key in campos]
        cursor.execute(insert_query, values)
    conn.commit()
    messagebox.showinfo("Sucesso", f'Dados inseridos na tabela {table_name} com sucesso.')

def enviar_requisicoes():
    # Obtém os valores inseridos pelo usuário
    driver = entry_driver.get()
    server = entry_server.get()
    database = entry_database.get()
    username = entry_username.get()
    password = entry_password.get()
    url = entry_url.get()
    dias = int(entry_dias.get())
    limite = int(entry_limite.get())  # Obtém o limite inserido pelo usuário
    nome_tabela = entry_nome_tabela.get()  # Obtém o nome da tabela inserido pelo usuário

    # Calcula as datas com base nos dias inseridos
    data_atual = datetime.now()
    data_d1 = data_atual - timedelta(days=1)
    data_d2 = data_atual - timedelta(days=dias)

    # Parâmetros da requisição
    params = {
        "data_inicial": data_d2.strftime("%Y-%m-%d"),
        "data_final": data_d1.strftime("%Y-%m-%d"),
        "limite": limite  # Adiciona o limite à requisição
    }

    # Faz a requisição
    response = requests.post(url, json=params)

    if response.status_code == 200:
        # Conectar-se ao banco de dados SQL Server
        conn = create_connection(driver, server, database, username, password)
        if conn is not None:
            cria_tabela(response, conn, nome_tabela)
            insere_valores(response, conn, nome_tabela)
            alter_table_column_size(conn, nome_tabela, 'fotos', 'MAX')
            conn.close()
    else:
        messagebox.showerror("Erro", f"Erro ao enviar requisição. Código de status: {response.status_code}")

# Criando a janela principal
root = tk.Tk()
root.title("Interface para Requisição e Banco de Dados")

# Definindo o tamanho da janela
root.geometry("500x350")

# Criando os campos de entrada para os detalhes de conexão e URL
tk.Label(root, text="Driver:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_driver = tk.Entry(root)
entry_driver.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Server:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_server = tk.Entry(root)
entry_server.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Database:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_database = tk.Entry(root)
entry_database.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Username:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Password:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="URL da API:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
entry_url = tk.Entry(root)
entry_url.grid(row=5, column=1, padx=5, pady=5)

tk.Label(root, text="Dias:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
entry_dias = tk.Entry(root)
entry_dias.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Limite de requisições:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
entry_limite = tk.Entry(root)
entry_limite.grid(row=7, column=1, padx=5, pady=5)

tk.Label(root, text="Nome da Tabela:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
entry_nome_tabela = tk.Entry(root)
entry_nome_tabela.grid(row=8, column=1, padx=5, pady=5)

# Botão para enviar as requisições
tk.Button(root, text="Enviar Requisições", command=enviar_requisicoes).grid(row=9, columnspan=2, pady=12)

root.mainloop()
