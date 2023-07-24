#Criação da tabela: stg_faixas

import pandas as pd
from datetime import datetime

import sys
sys.path.append('../libs')
from fn_database import conectar
from fn_database import executar_consulta
from fn_database import inserir_dados
from api_youtube import get_publish_info


#Criando tabela
conexao = conectar('bronze_youtube')
faixas = executar_consulta(conexao,"SELECT DISTINCT idVideo, titulo FROM bronze_youtube.raw_webscrapping_youtube")

#Pegando dados da API
faixas["publishedAt"] = faixas["idVideo"].apply(get_publish_info)


# Cria a tabela
conexao = conectar('silver_youtube')
inserir_dados(conexao, 'stg_faixas', [f"`{col}` VARCHAR(1000)" for col in faixas.columns], dados = faixas.values.tolist())