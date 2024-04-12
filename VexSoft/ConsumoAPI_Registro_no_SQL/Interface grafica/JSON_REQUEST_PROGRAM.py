import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests
import pyodbc
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
                for _ in range(num_requests):
                    data_atual = datetime.now()
                    data_d1 = data_atual - timedelta(days=1)
                    data_d2 = data_atual - timedelta(days=2)

                    params = {
                        "data_inicial": data_d2.strftime("%Y-%m-%d"),
                        "data_final": data_d1.strftime("%Y-%m-%d"),
                        "limite": 5
                    }

                    response = requests.post(url, json=params)
                    if response.status_code == 200:
                        self.log("Request successful.")
                        if conn:
                            self.cria_tabela(response, conn, table_name)
                            self.insere_valores(response, conn, table_name)
                    else:
                        self.log(f"Request failed. Status code: {response.status_code}")
                self.log("Requests completed.")
                time.sleep(60)  # Wait for one minute before checking time again
        conn.close()

root = tk.Tk()
app = App(root)
root.mainloop()
