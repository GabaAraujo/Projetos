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
    "data_inicial": "2023-01-01",
    "data_final": "2023-12-31",
    "limite": 10
}

# Enviar a requisição POST
response = requests.post(url, json=params)

# Verificar se a requisição foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Exibir a resposta da requisição
    data = response.json()

    print(data)

    # Conectar-se ao banco de dados SQL Server
    conn = create_connection(
        driver='{SQL Server}',  # substitua pelo driver adequado
        server='18.229.225.139',
        database='BMCLIENTES',
        username='api_vex',
        password='hexagon@vex'
    )

    # SQL para criar a tabela
    sql_create_table = """

   IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'registro')
BEGIN

CREATE TABLE registro(
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
    versao_app VARCHAR(255),
    frota VARCHAR(255),
    data_sincronizacao DATETIME,
    motorista VARCHAR(255),
    cliente VARCHAR(255),
    responsavel VARCHAR(255),
    responsavel_rg VARCHAR(255),
    retirar_pertences VARCHAR(255),
    tipo_veiculo VARCHAR(255),
    cor VARCHAR(255),
    qtde_pneus INT,
    pneu_dianteiro_esquerdo_marca VARCHAR(255),
    pneu_traseiro_esquerdo_marca VARCHAR(255),
    pneu_dianteiro_direito_marca VARCHAR(255),
    pneu_traseiro_direito_marca VARCHAR(255),
    pneu_dianteiro_esquerdo_situacao VARCHAR(255),
    pneu_traseiro_esquerdo_situacao VARCHAR(255),
    pneu_dianteiro_direito_situacao VARCHAR(255),
    pneu_traseiro_direito_situacao VARCHAR(255),
    estepe_marca VARCHAR(255),
    estepe_situacao VARCHAR(255),
    local_vistoria VARCHAR(255),
    contato_local VARCHAR(255),
    cidade VARCHAR(255),
    destino VARCHAR(255),
    destino_cidade VARCHAR(255),
    exportada VARCHAR(255),
    data_exportacao DATETIME,
    responsavel_entrega VARCHAR(255),
    responsavel_entrega_rg VARCHAR(255),
    responsavel_entrega_email VARCHAR(255),
    responsavel_telefone VARCHAR(255),
    token_vistoria VARCHAR(255),
    device_id VARCHAR(255),
    nivel_gnv INT,
    documento_gnv_atualizado VARCHAR(255),
    capacidade_gnv VARCHAR(255),
    versao_app_code INT,
    versao_app_name VARCHAR(255),
    ano_documento_crlv INT,
    id_questionario INT,
    id_status INT,
    situacao_veiculo VARCHAR(255),
    situacao_local_atendimento VARCHAR(255),
    id_pre_vistoria INT,
    observacao_status VARCHAR(255),
    observacao_coleta VARCHAR(255),
    existe_diretorio VARCHAR(255),
    contingencia INT,
    qtde_avarias_fotos INT,
    qtde_avarias_questionario INT,
    qtde_avarias_total INT,
    origem VARCHAR(255),
    sincronizacao_data DATETIME,
    bateria VARCHAR(255),
    crlv VARCHAR(255),
    coord_gps VARCHAR(255),
    marca_bateria VARCHAR(255),
    pesquisa_satisfacao VARCHAR(255),
    servico VARCHAR(255),
    ano_veiculo INT,
    nome_veiculo VARCHAR(255),
    contrato VARCHAR(255),
    data_assinatura_entrega DATETIME,
    fone_cliente VARCHAR(255),
    valor_servico VARCHAR(255),
    id_ultima_vistoria_placa INT,
    tipovistoria_ultima_vistoria_placa VARCHAR(255),
    data_fim DATETIME,
    hora_fim TIME,
    produto VARCHAR(255),
    retirar VARCHAR(255),
    sinistro VARCHAR(255),
    versaoDeDados VARCHAR(255),
    mes_sincronizacao INT,
    ano_sincronizacao INT,
    json_removido INT,
    data_hora_fim_upload DATETIME,
    horimetro2 VARCHAR(255),
    possui_divergencia INT,
    qtde_fotos INT,
    qtde_perguntas INT,
    id_tipo_operacao INT,
    id_tipo_operacao_ultima_vistoria_placa INT,
    endereco_gps VARCHAR(255),
    patio_processado INT,
    ano INT,
    mes INT,
    vistoriador_cnpj VARCHAR(255),
    vistoriador_uf VARCHAR(255),
    vistoriador_municipio VARCHAR(255),
    url_download VARCHAR(255),
    fotos VARCHAR(max),
    campos_personalizaveis VARCHAR(max)
);
END;
    """

    # Criar a tabela
    if conn is not None:
        # Criar a tabela
        conn.execute(sql_create_table)
        
        # Inserir os dados na tabela
        cursor = conn.cursor()
        for item in data: #pega os dados retornados do json
            cursor.execute("""
                INSERT INTO registro 
                (id, id_usuario, vistoriador, data, hora, email_cliente, placa, chassi, tipo_vistoria, km_odometro, horimetro, 
                nivel_combustivel, observacao, vistoria_id, id_empresa, email_enviado_cliente, token_empresa, versao_app)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (item['id'], item['id_usuario'], item['vistoriador'], item['data'], item['hora'], item['email_cliente'],
                item['placa'], item['chassi'], item['tipo_vistoria'], item['km_odometro'], item['horimetro'],
                item['nivel_combustivel'], item['observacao'], item['vistoria_id'], item['id_empresa'],
                item['email_enviado_cliente'], item['token_empresa'], item['versao_app']))
        conn.commit()
     
        print("Dados inseridos com sucesso no banco de dados")
    else:
        print("Erro! Não foi possível conectar-se ao banco de dados.")
else:
    # Se não for bem-sucedida, exibir o código de status
    print("Erro ao enviar requisição. Código de status:", response.status_code)


# Close the connection
conn.close()