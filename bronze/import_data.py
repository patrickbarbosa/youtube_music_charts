import pandas as pd
from datetime import datetime, timedelta

import sys
sys.path.append('../libs')
from fn_database import conectar
from fn_database import inserir_dados

from web_scrapping import webscrapping_yt



# Criar um DataFrame vazio com as colunas explicitadas
df = pd.DataFrame()

datMin = '2019-01-04'
datMax = '2023-06-02'


# Convertendo as strings para objetos datetime
datMax_dt = datetime.strptime(datMax, '%Y-%m-%d')
datMin_dt = datetime.strptime(datMin, '%Y-%m-%d')

artistas = []
while (datMax_dt >= datMin_dt):


    # Converte datMax_dt para um objeto date antes de somar o timedelta
    data_fim_semana = (datMax_dt + timedelta(days=6)).date()

    dados = webscrapping_yt(str(datMax_dt.date()),str(data_fim_semana))
    df = pd.concat([df,dados], ignore_index = True)

    print(f'Semana {datMax_dt} processada')

    # Diminui uma semana
    datMax_dt = datMax_dt - timedelta(days=7)


# Extrair o idVideo
df['idVideo'] = df['idVideo'].str.slice(start=len("https://www.youtube.com/watch?v="))


# Converter a coluna para o tipo string
df["artistas"] = df["artistas"].astype(str)
#Tratar caracteres
df['artistas'] = df['artistas'].str.replace("('", "").str.replace("',)", "").str.replace("', ', ', '",", ").str.replace("', ' & ', ",", ").str.replace(",'",", ").str.replace("')","").str.replace(", '",", ").str.replace(" ,",", ").str.replace(", ",",").str.replace("--,","")


# ALIMENTANDO O BANCO DE DADOS

# Conectando ao database
conexao = conectar('bronze_youtube')

# Adicionando data de Importação
df["import_date"] = datetime.now()

# Criar as tabelas
inserir_dados(conexao, 'raw_webscrapping_youtube', [f"`{col}` VARCHAR(1000)" for col in df.columns], dados = df.values.tolist())
