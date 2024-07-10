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



conn = create_connection(
    driver='{SQL Server}',
    server='GEO-WNB24020193',
    database='Teste',
    username='',
    password=''
)

if conn is not None:
    cursor = conn.cursor()

    cursor.execute("""
    SELECT [id]
          ,[campos_personalizaveis]
    FROM [Teste].[dbo].[Teste2]
    """)

    resultados = cursor.fetchall()  # Alteração aqui para fetchall()

    if resultados:  # Verifica se há resultados antes de continuar
        for linha in resultados:  # Itera sobre todas as linhas retornadas
            # Get the ID from the first element of the linha tuple
            id = linha[0] #recebe o primeiro dado

            # No need to convert the second element to a list of dictionaries since it's already a string
            dados_string = linha[1] #recebe o string
            # #\d é uma classe de caracteres de de 0 a 9, '([^']+): corresponde a qualquer sequência de caracteres sem apóstrofo ('), 
            # Extract and separate each value using regular expressions
            for match in re.finditer(r"{'id_campo': (\d+), 'descricao': '([^']+)', 'resposta': '([^']+)'}", dados_string):
                id_campo = match.group(1)
                descricao = match.group(2)
                resposta = match.group(3)

                print(f"ID: {id}")
                print(f"ID Campo: {id_campo}")
                print(f"Descrição: {descricao}")
                print(f"Resposta: {resposta}")
                print("-------------------------")
    else:
        print("Nenhum resultado encontrado.")

    # Fechar conexão
    conn.close()
else:
    print("Falha ao conectar ao banco de dados.")
