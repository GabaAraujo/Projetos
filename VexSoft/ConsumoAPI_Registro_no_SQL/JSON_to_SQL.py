import requests
import pyodbc

# Função para criar uma conexão com o banco de dados SQL Server
def create_connection(driver, server, database, username, password):
    conn = None
    try:
        conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}")
        print("Conexão com o banco de dados SQL Server bem-sucedida")
    except pyodbc.Error as e:
        print(e)
    return conn

# URL da API
url = "https://apiv3.vexsoft.com.br/vistoria/axn105"

# Parâmetros da requisição
params = {
    "data_inicial": "2023-12-01",
    "data_final": "2023-12-31",
    "limite": 1
}

# Enviar a requisição POST
response = requests.post(url, json=params)

# Verificar se a requisição foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Exibir a resposta da requisição
    data = response.json()

    #print(data)

    # Conectar-se ao banco de dados SQL Server
    conn = create_connection(
        driver='{SQL Server}',  # substitua pelo driver adequado
        server='GEO-WNB24020193',
        database='Teste',
        username='',
        password=''
    )

    # SQL para criar a tabela
    sql_create_table = """
    CREATE TABLE registros (
        id INT,
        id_usuario INT,
        vistoriador VARCHAR(255),
        data DATETIME,
        hora TIME,
        email_cliente VARCHAR(255),
        placa VARCHAR(255),
        chassi VARCHAR(255),
        tipo_vistoria VARCHAR(255),
        km_odometro INT,
        horimetro INT,
        nivel_combustivel INT,
        observacao TEXT,
        vistoria_id VARCHAR(255),
        id_empresa INT,
        email_enviado_cliente INT,
        token_empresa VARCHAR(255),
        versao_app VARCHAR(255)
       
    );
    """

    # Criar a tabela
    if conn is not None:
        # Criar a tabela
        conn.execute(sql_create_table)
        
        # Inserir os dados na tabela
        cursor = conn.cursor()
        for item in data: #pega os dados retornados do json
            cursor.execute("""
                INSERT INTO registros 
                (id, id_usuario, vistoriador, data, hora, email_cliente, placa, chassi, tipo_vistoria, km_odometro, horimetro, 
                nivel_combustivel, observacao, vistoria_id, id_empresa, email_enviado_cliente, token_empresa, versao_app)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (item['id'], item['id_usuario'], item['vistoriador'], item['data'], item['hora'], item['email_cliente'],
                item['placa'], item['chassi'], item['tipo_vistoria'], item['km_odometro'], item['horimetro'],
                item['nivel_combustivel'], item['observacao'], item['vistoria_id'], item['id_empresa'],
                item['email_enviado_cliente'], item['token_empresa'], item['versao_app']))
        conn.commit()
        conn.close()
        print("Dados inseridos com sucesso no banco de dados")
    else:
        print("Erro! Não foi possível conectar-se ao banco de dados.")
else:
    # Se não for bem-sucedida, exibir o código de status
    print("Erro ao enviar requisição. Código de status:", response.status_code)