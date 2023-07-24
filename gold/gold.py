#Criação de tabelas GOLD (Usuário final)

import pandas as pd

import sys
sys.path.append('../libs')
from fn_database import conectar
from fn_database import executar_consulta
from fn_database import inserir_dados


#Criando tabela
conexao = conectar('silver_youtube')
tb_dm_artistas = executar_consulta(conexao,'SELECT * FROM silver_youtube.stg_artistas')
tb_dm_faixas = executar_consulta(conexao,'SELECT * FROM silver_youtube.stg_faixas')
tb_dm_artista_faixa = executar_consulta(conexao,'SELECT * FROM silver_youtube.stg_faixa_artista')


# Inserindo as tabelas "dimensão"
conexao = conectar('gold_youtube')
inserir_dados(conexao, 'tb_dm_artistas', [f"`{col}` VARCHAR(1000)" for col in tb_dm_artistas.columns], dados = tb_dm_artistas.values.tolist())
inserir_dados(conexao, 'tb_dm_faixas', [f"`{col}` VARCHAR(1000)" for col in tb_dm_faixas.columns], dados = tb_dm_faixas.values.tolist())
inserir_dados(conexao, 'tb_dm_artista_faixa', [f"`{col}` VARCHAR(1000)" for col in tb_dm_artista_faixa.columns], dados = tb_dm_artista_faixa.values.tolist())


# Criando a tabela "fato"
conexao = conectar('silver_youtube')
query = '''SELECT    
	A.Semana   
	, A.fimSemana   
	, A.Posicao_Semana   
	, A.Posicao_Semana_Anterior   
	, A.idVideo   
	, A.varViews   
	, A.views         
	, A.Semanas_Chart   
	, CASE 
		WHEN B.publishedAt BETWEEN A.Semana AND A.fimSemana THEN 1    
		ELSE 0     
		END AS flg_Lancamento_Semana   
	, CASE     
		WHEN TIMESTAMPDIFF(MONTH, B.publishedAt, A.Semana) < 42 THEN 'Frontline'    
		ELSE 'Catálogo'    
		END AS Classificacao
    ,MIN(Semana) OVER (PARTITION BY idVideo) AS Semana_Entrada_Charts  
	FROM stg_charts A
	INNER JOIN stg_faixas B   
		ON A.idVideo = B.idVideo '''

tb_fato_charts =  executar_consulta(conexao,query)

conexao = conectar('gold_youtube')
inserir_dados(conexao, 'tb_fato_charts', [f"`{col}` VARCHAR(1000)" for col in tb_fato_charts.columns], dados = tb_fato_charts.values.tolist())