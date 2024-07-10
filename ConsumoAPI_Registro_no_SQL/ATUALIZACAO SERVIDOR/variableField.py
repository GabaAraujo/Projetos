import pyodbc
import json

def create_connection(driver, server, database, username, password):
    connection_string = f"""
        DRIVER={driver};
        SERVER={server};
        DATABASE={database};
        UID={username};
        PWD={password};
    """
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")
        return conn
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

def fetch_and_insert_data(conn):
    select_query = "SELECT [id], [campos_personalizaveis] FROM [BMCLIENTES].[dbo].[BdVexSoft]"
    
    # Mapping descriptions to column names
    description_to_column = {
        'Placa do veículo': 'placa_veiculo',
        'Placa do equipamento': 'placa_equipamento',
        'Empresa do veículo': 'empresa_veiculo',
        'Tipo de equipamento': 'tipo_equipamento',
        'Fabricante': 'fabricante',
        'Modelo': 'modelo',
        'Técnico executante 1': 'tecnico_executante_1',
        'Técnico executante 2': 'tecnico_executante_2',
        'Técnico executante 3': 'tecnico_executante_3',
        'Qual o produto instalado?': 'produto_instalado',
        'Número Serial Antena': 'numero_serial_antena',
        'Número Serial Display': 'numero_serial_display',
        'Número Serial Main Unit': 'numero_serial_main_unit',
        'Instalação com Antena Beacon': 'instalacao_com_antena_beacon',
        'Número Serial Antena Beacon': 'numero_serial_antena_beacon',
        'Horário - Aguardando veículo': 'horario_aguardando_veiculo',
        'Horário - Início da atividade': 'horario_inicio_atividade',
        'Horário - Fim da atividade': 'horario_fim_atividade',
        'Horário - Fim da configuração': 'horario_fim_configuracao',
        'Qual o fabricante?': 'qual_o_fabricante',
        'Tipo de manutenção': 'tipo_de_manutencao',
        'Falha encontrada': 'falha_encontrada',
        'Tipo de falha': 'tipo_de_falha',
        'Solução aplicada': 'solucao_aplicada',
        'Serial Main Unit retirada': 'serial_main_unit_retirada',
        'Item substituído 1': 'item_substituido_1',
        'Item substituído 2': 'item_substituido_2'
    }
    
    insert_query = """
    INSERT INTO dbo.valores_dinamicos (
        id, placa_veiculo, placa_equipamento, empresa_veiculo, tipo_equipamento, fabricante, modelo,
        tecnico_executante_1, tecnico_executante_2, tecnico_executante_3, produto_instalado, 
        numero_serial_antena, numero_serial_display, numero_serial_main_unit, instalacao_com_antena_beacon, 
        numero_serial_antena_beacon, horario_aguardando_veiculo, horario_inicio_atividade, horario_fim_atividade, 
        horario_fim_configuracao, qual_o_fabricante, tipo_de_manutencao, falha_encontrada, tipo_de_falha, 
        solucao_aplicada, serial_main_unit_retirada, item_substituido_1, item_substituido_2
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    check_query = "SELECT COUNT(*) FROM dbo.valores_dinamicos WHERE id = ?"
    
    try:
        cursor = conn.cursor()
        cursor.execute(select_query)
        rows = cursor.fetchall()
        
        for row in rows:
            id_value = row.id
            campos_personalizaveis = row.campos_personalizaveis
            
            # Check if the ID already exists in the valores_dinamicos table
            cursor.execute(check_query, id_value)
            if cursor.fetchone()[0] > 0:
                print(f"ID {id_value} already exists, skipping insertion.")
                continue
            
            # Initialize a dictionary with None (for NULL values)
            data_dict = {column: None for column in description_to_column.values()}
            
            try:
                # Extract JSON-like string from database field
                start_index = campos_personalizaveis.find("[")
                end_index = campos_personalizaveis.rfind("]") + 1
                json_string = campos_personalizaveis[start_index:end_index]
                
                # Parse JSON data
                data = json.loads(json_string.replace("'", '"'))
                
                for item in data:
                    descricao = item.get('descricao', None)
                    resposta = item.get('resposta', None)
                    
                    if descricao and resposta:
                        column_name = description_to_column.get(descricao, None)
                        if column_name:
                            data_dict[column_name] = resposta
                
                cursor.execute(insert_query, id_value, *data_dict.values())
                conn.commit()
                print(f"Data inserted for id: {id_value}")
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error parsing JSON for id {id_value}: {e}")
    
    except pyodbc.Error as e:
        print(f"Error: {e}")

conn = create_connection(
    driver='{SQL Server}',  # Substitute with the appropriate driver
    server='18.229.225.139',
    database='BMCLIENTES',
    username='api_vex',
    password='hexagon@vex'
)

if conn:
    fetch_and_insert_data(conn)
    conn.close()
