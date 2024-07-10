import requests
import pyodbc


driver='{SQL Server}',  # substitua pelo driver adequado
server='GEO-WNB24020193',
database='Teste',
username='',
password=''

# URL da API
url = "https://apiv3.vexsoft.com.br/vistoria/axn105"

# Parâmetros da requisição
params = {
   "data_inicial": "2024-04-24",
    "data_final": "2025-04-23",
    "limite": 1
}

# Enviar a requisição POST
response = requests.post(url, json=params)


print(response)


if response.status_code == 200: #caso o  dado da resposta der certo
    print("ola")

    data = response.json()

    print(data)