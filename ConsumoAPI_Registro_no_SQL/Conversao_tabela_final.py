import pyodbc
import re

def create_connection(driver, server, database, username, password):
    conn = None
    try:
        conn = pyodbc.connect(f"Driver={driver};Server={server};Database={database};UID={username};PWD={password}")
        print("Conexão com o banco de dados SQL Server bem-sucedida")
    except pyodbc.Error as e:
        print(e)
    return conn

def registra_dados(table_name, ids, descricoes, respostas, conn):
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT count([id])
    FROM [BdVexSoft]
    """)
    valores_a_repetir = int(cursor.fetchone()[0])  # Pegando o valor das linhas
    incremento = 15

    for x in range(valores_a_repetir):  # Iterando apenas 15 vezes
            query =  f"""INSERT INTO {table_name}(ID,
        [{descricoes[0]}], [{descricoes[1]}], [{descricoes[2]}],
        [{descricoes[3]}], [{descricoes[4]}],[{descricoes[5]}], 
        [{descricoes[6]}], [{descricoes[7]}],[{descricoes[8]}], 
        [{descricoes[9]}], [{descricoes[10]}],[{descricoes[11]}], 
        [{descricoes[12]}], [{descricoes[13]}],[{descricoes[14]}]
        )
        VALUES
        ('{ids[0 + (incremento * x)]}', 
        '{respostas[0 + (incremento * x)]}', '{respostas[1 + (incremento * x)]}', '{respostas[2 + (incremento * x)]}',
        '{respostas[3 + (incremento * x)]}', '{respostas[4 + (incremento * x)]}', '{respostas[5 + (incremento * x)]}',
        '{respostas[6 + (incremento * x)]}', '{respostas[7 + (incremento * x)]}', '{respostas[8 + (incremento * x)]}',
        '{respostas[9 + (incremento * x)]}', '{respostas[10 + (incremento * x)]}', '{respostas[11 + (incremento * x)]}',
        '{respostas[12 + (incremento * x)]}', '{respostas[13 + (incremento * x)]}', '{respostas[14 + (incremento * x)]}')"""

            cursor.execute(query) #executa chamando o cursor->(cursor seria o terminal do sql server)
            conn.commit() #comita -> faz a execução
            print("Dados inseridos com sucesso")

    #campos = []
    #campos.append(descricoes[0:15]) # pega os nomes do campo
    #insert_query = f"INSERT INTO {table_name} ({', '.join(campos)}) VALUES ({', '.join(['?' for _ in campos])})"

conn = create_connection(
    driver='{SQL Server}',
    #server='GEO-WNB24020193',
    #database='Teste',
    #username='',
    #password=''
    server='18.229.225.139',
    database='BMCLIENTES',
    username='api_vex',
    password='hexagon@vex'
)

if conn is not None:
    cursor = conn.cursor()
    cursor.execute("""
  SELECT [id]
          ,[campos_personalizaveis]
    FROM [BdVexSoft] 
    WHERE[campos_personalizaveis] LIKE '%''descricao'': ''Técnico executante 3'', ''resposta'': ''''%'
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
    table_name = "valores_dinamicos"
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

        cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        if cursor.fetchone()[0] == 0:
            columns = ','.join([f'[{desc}] VARCHAR(8000)' for desc in descricoes[:15]])
            create_table_query = f'CREATE TABLE {table_name} (ID INT, {columns})'
            cursor.execute(create_table_query)
            conn.commit()
            print(f'Table {table_name} created successfully with columns: {"ID, " + ", ".join(descricoes[:15])}')
            registra_dados(table_name,ids,descricoes,respostas,conn)  

        else:
            print(f'Table {table_name} already exists.')
            registra_dados(table_name,ids,descricoes,respostas,conn)  

    else:
        print("Nenhum resultado encontrado.")

    conn.close()
else:
    print("Falha ao conectar ao banco de dados.")
