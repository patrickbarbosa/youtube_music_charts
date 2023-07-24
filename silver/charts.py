#Criação da tabela: stg_charts

import pandas as pd

import sys
sys.path.append('../libs')
from fn_database import conectar
from fn_database import executar_consulta
from fn_database import inserir_dados


#Criando tabela
conexao = conectar('bronze_youtube')




query = '''
	SELECT 
		A.iniSemana AS Semana
		, A.fimSemana
		, A.classificacao AS Posicao_Semana
		, A.semanaPassada AS Posicao_Semana_Anterior
		, A.idVideo
		, A.varViews
		, A.views
        , A.semanas AS Semanas_Chart
	FROM bronze_youtube.raw_webscrapping_youtube A
'''
charts = executar_consulta(conexao,query)


# Convertendo colunas
charts["varViews"] = pd.to_numeric(charts["varViews"])
charts["views"] = pd.to_numeric(charts["views"])


charts["varViews"] = charts["varViews"]/100.0


# Cria a tabela
conexao = conectar('silver_youtube')
inserir_dados(conexao, 'stg_charts', [f"`{col}` VARCHAR(1000)" for col in charts.columns], dados = charts.values.tolist())



