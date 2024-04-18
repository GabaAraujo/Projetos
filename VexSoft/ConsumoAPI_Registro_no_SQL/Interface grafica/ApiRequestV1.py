import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
import pyodbc
import re
from datetime import datetime, timedelta
import time
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("API Request App")
        
        self.url_label = tk.Label(root, text="URL:")
        self.url_label.grid(row=0, column=0, sticky="w")
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2)

        self.server_label = tk.Label(root, text="Server:")
        self.server_label.grid(row=1, column=0, sticky="w")
        self.server_entry = tk.Entry(root, width=50)
        self.server_entry.grid(row=1, column=1, columnspan=2)

        self.database_label = tk.Label(root, text="Database:")
        self.database_label.grid(row=2, column=0, sticky="w")
        self.database_entry = tk.Entry(root, width=50)
        self.database_entry.grid(row=2, column=1, columnspan=2)

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=3, column=0, sticky="w")
        self.username_entry = tk.Entry(root, width=50)
        self.username_entry.grid(row=3, column=1, columnspan=2)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=4, column=0, sticky="w")
        self.password_entry = tk.Entry(root, show="*", width=50)
        self.password_entry.grid(row=4, column=1, columnspan=2)

        self.requests_label = tk.Label(root, text="Number of Requests:")
        self.requests_label.grid(row=5, column=0, sticky="w")
        self.requests_entry = tk.Entry(root)
        self.requests_entry.grid(row=5, column=1, columnspan=2)

        self.time_label = tk.Label(root, text="Time to Run (HH:MM):")
        self.time_label.grid(row=6, column=0, sticky="w")
        self.time_entry = tk.Entry(root)
        self.time_entry.grid(row=6, column=1, columnspan=2)

        self.table_label = tk.Label(root, text="Table Name:")
        self.table_label.grid(row=7, column=0, sticky="w")
        self.table_entry = tk.Entry(root)
        self.table_entry.grid(row=7, column=1, columnspan=2)

        self.log_label = tk.Label(root, text="Log:")
        self.log_label.grid(row=8, column=0, sticky="w")
        self.log_text = scrolledtext.ScrolledText(root, width=60, height=10)
        self.log_text.grid(row=8, column=1, columnspan=2)

        self.start_button = tk.Button(root, text="Start", command=self.start_program)
        self.start_button.grid(row=9, column=1, sticky="w")
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_program, state=tk.DISABLED)
        self.stop_button.grid(row=9, column=2, sticky="e")

        self.running = False
        self.thread = None



    def limpa_tabela(self, tabela_nova,conn):    
        cursor = conn.cursor()

        query_delete = f"DELETE FROM [{tabela_nova}]"
        cursor.execute(query_delete)
        conn.commit()

        # Fechar o cursor após a execução da consulta
        cursor.close()




    def registra_dados_dinamicos(self, table_name,tabela_nova, ids, descricoes, respostas, conn):
        cursor = conn.cursor()
        cursor.execute(f"""
        SELECT count([id])
        FROM [{table_name}]
        """)
     

      

        
        

        valores_a_repetir = int(cursor.fetchone()[0])  # Pegando o valor das linhas
        incremento = 15
   

        self.limpa_tabela(tabela_nova, conn)
        for x in range(valores_a_repetir):  # Iterando apenas 15 vezes
            query =  f"""INSERT INTO {tabela_nova}(ID,
            [{descricoes[0]}], [{descricoes[1]}], [{descricoes[2]}],
            [{descricoes[3]}], [{descricoes[4]}],[{descricoes[5]}], 
            [{descricoes[6]}], [{descricoes[7]}],[{descricoes[8]}], 
            [{descricoes[9]}], [{descricoes[10]}],[{descricoes[11]}], 
            [{descricoes[12]}], [{descricoes[13]}],[{descricoes[14]}])
            VALUES
            ('{ids[0 + (incremento * x)]}', 
            '{respostas[0 + (incremento * x)]}', '{respostas[1 + (incremento * x)]}', '{respostas[2 + (incremento * x)]}',
            '{respostas[3 + (incremento * x)]}', '{respostas[4 + (incremento * x)]}', '{respostas[5 + (incremento * x)]}',
            '{respostas[6 + (incremento * x)]}', '{respostas[7 + (incremento * x)]}', '{respostas[8 + (incremento * x)]}',
            '{respostas[9 + (incremento * x)]}', '{respostas[10 + (incremento * x)]}', '{respostas[11 + (incremento * x)]}',
            '{respostas[12 + (incremento * x)]}', '{respostas[13 + (incremento * x)]}', '{respostas[14 + (incremento * x)]}')"""


            #print(query)
            try:
               
               
                cursor.execute(query) #executa chamando o cursor->(cursor seria o terminal do sql server)
                conn.commit() #comita -> faz a execução
                self.log(f"Dados inseridos com sucesso na tabela {tabela_nova}")
            except pyodbc.Error as e:
                conn.rollback()
                self.log(f"Erro ao inserir dados: {e}")


    

    def registra_campos_dinamicos(self, conn, table_name, tabela_nova): 
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT [id]
                ,[campos_personalizaveis]
            FROM [{table_name}] 
            WHERE [campos_personalizaveis] LIKE '%''descricao'': ''Técnico executante 3'', ''resposta'': ''''%'
            AND [campos_personalizaveis] LIKE '%''Placa do veículo''%'
            AND [campos_personalizaveis] LIKE '%''Empresa do veículo''%'
            AND [campos_personalizaveis] LIKE '%''Tipo de equipamento''%'
            AND [campos_personalizaveis] LIKE '%''Fabricante''%'
            AND [campos_personalizaveis] LIKE '%''Modelo''%'
            AND [campos_personalizaveis] LIKE '%''Técnico executante 1''%'
            AND [campos_personalizaveis] LIKE '%''Técnico executante 2''%'
            AND [campos_personalizaveis] LIKE '%''Qual o produto instalado?''%'
            AND [campos_personalizaveis] LIKE '%''Número Serial Antena''%'
            AND [campos_personalizaveis] LIKE '%''Número Serial Display''%'
            AND [campos_personalizaveis] LIKE '%''Número Serial Main Unit''%'
            AND [campos_personalizaveis] LIKE '%''Horário - Aguardando veículo''%'
            AND [campos_personalizaveis] LIKE '%''Horário - Início da atividade''%'
            AND [campos_personalizaveis] LIKE '%''Horário - Fim da atividade''%'
            AND [campos_personalizaveis] LIKE '%''Horário - Fim da configuração''%'
            """)
        
        resultados = cursor.fetchall()

        if resultados:
            ids = []
            id_campos = []
            descricoes = []
            respostas = []
            for resultado in resultados:
                id = resultado[0]
                dados_string = resultado[1]
                count = 0
                for match in re.finditer(r"{'id_campo': (\d+), 'descricao': '([^']+)', 'resposta': '([^']+)'}", dados_string):
                    id_campo = match.group(1)
                    descricao = match.group(2)
                    resposta = match.group(3)
                    ids.append(id)
                    id_campos.append(id_campo)
                    descricoes.append(descricao)
                    respostas.append(resposta)

            cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tabela_nova}'")
            if cursor.fetchone()[0] == 0:
                columns = ','.join([f'[{desc}] VARCHAR(8000)' for desc in descricoes[:16]])
                create_table_query = f'CREATE TABLE {tabela_nova} (ID INT, {columns})'
                print(create_table_query)
                cursor.execute(create_table_query)
                conn.commit()
                print(f'Table {tabela_nova} created successfully with columns: {"ID, " + ", ".join(descricoes[:16])}')
                self.registra_dados_dinamicos(table_name,tabela_nova, ids, descricoes, respostas, conn)  #pega todo os dados que estao no banco

            else:
                print(f'Table {tabela_nova} already exists.')
                self.registra_dados_dinamicos(table_name,tabela_nova, ids, descricoes, respostas, conn) 
        
        else:
            print("Nenhum resultado encontrado.")

    def start_program(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=self.run_program)
            self.thread.start()
        else:
            messagebox.showwarning("Warning", "Program is already running.")

    def stop_program(self):
        if self.running:
            self.running = False
            self.thread.join()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Warning", "Program is not running.")

    def log(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.log_text.insert(tk.END, f"{timestamp} {message}\n")
        self.log_text.see(tk.END)

    def create_connection(self, driver, server, database, username, password):
        conn = None
        try:
            conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}")
            self.log("Connection to SQL Server successful")
        except pyodbc.Error as e:
            self.log(f"Error connecting to SQL Server: {e}")
        return conn

    def cria_tabela(self, response, conn, table_name):
        response_data = response.json()
        campos = response_data[0].keys()

        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        if cursor.fetchone()[0] == 0:
            columns = ','.join([f'[{campo}] VARCHAR(8000)' for campo in campos])
            create_table_query = f'CREATE TABLE {table_name} ({columns})'
            cursor.execute(create_table_query)
            conn.commit()
            self.log(f"Table {table_name} created successfully with columns: {', '.join(campos)}")
        else:
            self.log(f"Table {table_name} already exists.")

    def alter_table_column_size(self, conn, table_name, column_name, new_size):
        cursor = conn.cursor()
        alter_query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} VARCHAR({new_size})"
        cursor.execute(alter_query)
        conn.commit()
        self.log(f"Column {column_name} in table {table_name} altered successfully with size {new_size}.")

    def insere_valores(self, response, conn, table_name):
        response_data = response.json()
        campos = response_data[0].keys()

        cursor = conn.cursor()
        insert_query = f"INSERT INTO {table_name} ({', '.join(campos)}) VALUES ({', '.join(['?' for _ in campos])})"
        for row in response_data:
            values = [str(row[key]) for key in campos]
            cursor.execute(insert_query, values)
        conn.commit()
        self.log(f"Data inserted into {table_name} successfully.")

    def run_program(self):
        url = self.url_entry.get()
        num_requests = int(self.requests_entry.get())
        time_to_run = self.time_entry.get()
        table_name = self.table_entry.get()

        conn = self.create_connection(
            driver='{SQL Server}',
            server=self.server_entry.get(),
            database=self.database_entry.get(),
            username=self.username_entry.get(),
            password=self.password_entry.get()
        )

        while self.running:
            now = datetime.now().strftime("%H:%M")
            if now == time_to_run:
                self.log("Starting requests...")
                
                data_atual = datetime.now()
                data_d1 = data_atual - timedelta(days=1)
                data_d2 = data_atual - timedelta(days=2)

                params = {
                        "data_inicial": data_d2.strftime("%Y-%m-%d"),
                        "data_final": data_d1.strftime("%Y-%m-%d"),
                        "limite": num_requests
                    }

                response = requests.post(url, json=params)
                if response.status_code == 200:
                        self.log("Request successful.")
                        if conn:
                            self.cria_tabela(response, conn, table_name)
                            self.insere_valores(response, conn, table_name)
                            self.registra_campos_dinamicos(conn, table_name,"valores_dinamicos")
                else:
                        self.log(f"Request failed. Status code: {response.status_code}")
                self.log("Requests completed.")
                time.sleep(60)  # Wait for one minute before checking time again
        conn.close()

root = tk.Tk()
app = App(root)
root.mainloop()
